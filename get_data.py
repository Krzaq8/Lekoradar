from database.connection import connection

query = '''SELECT 
  M.id, 
  M.name, 
  I.form, 
  I.dose, 
  M.quantity, 
  M.id_code, 
  M.refund_scope, 
  M.refund, 
  M.surcharge, 
  I.id
FROM 
  Medicine M, 
  Ingredient I, 
  Active_substance A
WHERE 
  I.id = M.ingredient
  AND I.active_substance = A.id
  AND A.name LIKE \'{}\'
ORDER BY 
  I.id
  '''

count_no = 0
ingr_no = 9
quantity_no = 4
surcharge_no = 8

result_heading = ['Numer grupy', 'Nazwa', 'Postać', 'Dawka', 'Zawartość opakowania', 
  'Numer GTIN lub inny kod jednoznacznie identyfikujący produkt', 'Zakres wskazań objętych refundacją',
  'Poziom odpłatności', 'Wysokość dopłaty świadczeniobiorcy']

def get_result_table(sub):
    with connection() as con:
        data_tuples = con.execute(query.format(sub)).fetchall()
        
        if data_tuples == []:
            return [result_heading]

        data = [list(i) for i in data_tuples]
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
                data[group_start:group_end].sort(key=lambda med: med[surcharge_no]/med[quantity_no])
                group_start = group_end
                prev_ingr = row[ingr_no]
            row[count_no] = count
            group_end += 1

        data[group_start:group_end].sort(key=lambda med: med[surcharge_no]/med[quantity_no])

        return [result_heading] + [i[:-1] for i in data]

def get_substance_table():
    with connection() as con:
        query_result = con.execute('''SELECT name FROM Active_substance''').fetchall()
        return [list(substance)[0] for substance in query_result]

