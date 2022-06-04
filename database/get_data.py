import sys
sys.path.append('../')
from database.connection import connection, engine
from sqlalchemy import MetaData, select


result_heading = ['Numer grupy', 'Nazwa', 'Postać', 'Droga podania', 'Dawka', 'Zawartość opakowania', 
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
def get_result_table(substance):
  query = \
    select(
      I.c.id, 
      M.c.name, 
      F.c.name, 
      W.c.name, 
      I.c.dose,
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
