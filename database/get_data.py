import sys
sys.path.append('../')
from database.connection import connection, engine
from sqlalchemy import MetaData, select


result_heading = ['Numer grupy', 'Postać', 'Droga podania', 'Dawka', 'Nazwa', 'Zawartość opakowania',
  'Numer GTIN lub inny kod jednoznacznie identyfikujący produkt', 'Zakres wskazań objętych refundacją',
  'Poziom odpłatności', 'Wysokość dopłaty świadczeniobiorcy', 'Opłacalność']

meta = MetaData(bind=engine)
meta.reflect()
A = meta.tables['active_substance']
W = meta.tables['way']
F = meta.tables['form']
I = meta.tables['ingredient']
M = meta.tables['medicine']


# Przygotowuje tabelę wynikową dla substancji o id = substance.
# Wysyła zapytanie do bazy danych skąd pobiera dane o lekach z daną substancją aktywną.
# Dodaje nagłówek tabeli z nazwami kolumn.
def get_result_table(substance, route=-1):
  query = \
    select(
      I.c.id, 
      F.c.name, 
      W.c.name, 
      I.c.dose,
      M.c.name, 
      M.c.contents,
      M.c.id_code,
      M.c.refund_scope,
      M.c.refund,
      M.c.surcharge,
      M.c.quantity)\
    .where(
      M.c.ingredient == I.c.id,
      I.c.form == F.c.id,
      F.c.way == W.c.id,
      I.c.active_substance == A.c.id,
      A.c.id == substance)\
    .order_by(
      I.c.id,
      M.c.surcharge / M.c.quantity)

  if route != -1:
    query = query.where(W.c.id == route)

  data = []
  with connection() as con:
    data = [list(tuple) for tuple in con.execute(query).fetchall()]
    
  prev_id = -1
  curr_id = 0
  first_quantity = 1.0

  for row in data:
    if prev_id != row[0]:
      prev_id = row[0]
      curr_id += 1
      first_quantity = row[-1]

    row[0] = curr_id
    quantity = row[-1]
    surcharge = row[-2]
    row[-1] = surcharge * first_quantity / quantity
  
  return [result_heading] + data


# Zwraca listę substancji aktywnych do wyboru.
def get_substance_table():
  with connection() as con:
    return con.execute(select(A)).fetchall()


# Zwraca nazwę substancji aktywnej o danym id.
def get_substance_name(id):
  with connection() as con:
    name, = con.execute(select(A.c.name).where(A.c.id == id)).fetchall()[0]
    return name


# Zwraca listę możiwych dróg podania dla danej substancji (id, nazwa).
def get_routes_for_substance(id):
  with connection() as con:
    query = select(W).distinct().where(
      W.c.id == F.c.way,
      F.c.id == I.c.form,
      I.c.active_substance == id)
    return [(-1, 'wszystkie')] + con.execute(query).fetchall()
