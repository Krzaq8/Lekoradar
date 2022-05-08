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
  M.surcharge 
FROM 
  Medicine M, 
  Ingredient I 
WHERE 
  I.id = M.id 
  AND I.active_substance = {} 
ORDER BY 
  I.dose, 
  I.form'''

count_no = 0
form_no = 2
dose_no = 3
quantity_no = 4
surcharge_no = 8

def get_result_table(sub):
    with connection() as con:
        data_tuples = con.execute(query.format(sub)).fetchall()
        
        if data_tuples == []:
            return data_tuples

        data = [list(i) for i in data_tuples]
        group_start = 0
        group_end = 1
        count = 1
        data[0][count_no] = count
        prev_form = data[0][form_no]
        prev_dose = data[0][dose_no]

        for row in data[1:]:
            
            if row[form_no] != prev_form or row[dose_no] != prev_dose:
                # zmiana grupy odpowiedników
                count += 1
                # posortowanie grupy odpowiedników
                data[group_start:group_end].sort(key=lambda med: med[surcharge_no]/med[quantity_no])
                group_start = group_end
            row[count_no] = count
            group_end += 1

        data[group_start:group_end].sort(key=lambda med: med[surcharge_no]/med[quantity_no])

        return data

def get_substance_table():
    with connection() as con:
        subs_tuples = con.execute('''SELECT * FROM Active_substance''').fetchall
        return [list(sub) for sub in subs_tuples]
