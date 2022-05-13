from operator import and_
from database.connection import connection, engine
from sqlalchemy import MetaData, select

count_no = 0
ingr_no = 9
quantity_no = 4
surcharge_no = 8

result_heading = ['Numer grupy', 'Nazwa', 'Postać', 'Dawka', 'Zawartość opakowania', 
  'Numer GTIN lub inny kod jednoznacznie identyfikujący produkt', 'Zakres wskazań objętych refundacją',
  'Poziom odpłatności', 'Wysokość dopłaty świadczeniobiorcy']

meta = MetaData(bind=engine)
meta.reflect()
A = meta.tables['active_substance']
I = meta.tables['ingredient']
M = meta.tables['medicine']

def get_result_table(sub):
  query = select(M.c.id, M.c.name, I.c.form, I.c.dose, M.c.quantity, M.c.id_code, M.c.refund_scope, M.c.refund, M.c.surcharge, I.c.id)\
    .where(M.c.ingredient == I.c.id, I.c.active_substance == A.c.id, A.c.id == sub)\
    .order_by(I.c.id)

  data_tuples = []
  with connection() as con:
    data_tuples = con.execute(query).fetchall()
    
  if data_tuples == []:
    return [result_heading]

  data = [list(i) for i in data_tuples]
  data_c = []
  group_start = 0
  group_end = 1
  count = 1
  data[0][count_no] = count
  prev_ingr = data[0][ingr_no]

  for row in data[1:]:
    if row[ingr_no] != prev_ingr:
      # zmiana grupy odpowiedników
      count += 1
      # posortowanie grupy odpowiedników
      data_part = data[group_start:group_end]
      data_part.sort(key=lambda med: (float(med[surcharge_no]) / float(med[quantity_no])))
      data_c = data_c + data_part
      group_start = group_end
      prev_ingr = row[ingr_no]

    row[count_no] = count
    group_end += 1

  data_part = data[group_start:group_end]
  data_part.sort(key=lambda med: (float(med[surcharge_no]) / float(med[quantity_no])))
  data_c = data_c + data_part
  
  return [result_heading] + [i[:-1] for i in data_c]

def get_substance_table():
  with connection() as con:
    query_result = con.execute(select(A)).fetchall()
    return list(query_result)

def get_substance_name(id):
  with connection() as con:
    query_result = con.execute(select(A.c.name).where(A.c.id == id)).fetchall()
    (name,) = list(query_result)[0]
    return name
