import pandas as pd
import numpy as np
import re 
import sys
sys.path.append('../')

def remove_white_chars(text):
  p = 0
  q = len(text) - 1

  while p <= q and text[p] == ' ':
    p += 1
  while p <= q and text[q] == ' ':
    q -= 1

  return text[p:q + 1]

data_frame = pd.read_excel('source_data.xlsx', sheet_name='A1')
data_frame.to_csv('tmp_data.csv', index = None, header=False, sep='|')


raw_data = np.loadtxt("tmp_data.csv", skiprows = 1, delimiter = '|', dtype=str)
data = [[] for i in range(len(raw_data))]

active_substances = dict()
active_substances_r = dict()
substitute_groups = dict()
k = 0
l = 0
names_s = set()
doses_s = set()
forms = list()
forms_d = dict()

def add_form(new_form):
  global forms
  new_regex = new_form.replace('.', r'[a-ząćęńłśóżź]*\.? ?')
#  new_regex = new_form.replace('.', r'\.')
  matched = False

  for (regex, form) in forms:
    if re.fullmatch(regex, new_form):
      return form
    if re.fullmatch(new_regex, form):
      matched = True
      break

  if matched:
    forms = list(filter(lambda form: not re.fullmatch(new_regex, form[1]), forms))

  forms.append((new_regex, new_form))
  return new_form


# Pierwsza iteracja: zbieramy dane.
# Te których nie trzeba obrabiać od razu wrzucamy, resztę dodajemy do struktur.

for (i, med) in enumerate(raw_data):
  match = re.search(r'\d,\d', med[2])
  while match:
    idx = match.start() + 1
    med[2] = med[2][:idx] + '.' + med[2][idx + 1:]
    match = re.match(r'\d,\d', med[2])

  sth = med[2].split(',')
  name = sth[0]
  form = ''
  dose = ''

  for (j, form_trait) in enumerate(sth[1:]):
    if re.match(r'.*\d.*', form_trait):
      form = ','.join(sth[1:j + 1])
      dose = ','.join(sth[j + 1:])
      break

  dose = remove_white_chars(dose)
  old_form = remove_white_chars(form)
  form = add_form(old_form)

  if med[1] not in active_substances:
    k += 1
    active_substances[med[1]] = k
    active_substances_r[k] = med[1]
  as_id = active_substances[med[1]]

  quantity = list(map(int, re.findall(r'\d+', med[3])))[0]
  surcharge = float(med[15].replace(',', '.'))

  data[i] = [as_id, 0, name, old_form, dose, quantity, med[4], med[12], med[14], surcharge]
  names_s.add(name)
  doses_s.add(dose)


# W drugiej iteracji znamy już najkrótsze napisy postaci.
# Dla każdej takiej szukamy jej najdłuższego odpowiednika.
# Ponadto możemy podzielić już na grupy odpowiedników.

for i in range(len(data)):
  current_form = data[i][3]
  root_form = add_form(current_form)
  
  if root_form not in forms_d:
    forms_d[root_form] = current_form
  else:
    old_form = forms_d[root_form]
    if len(old_form) < len(current_form):
      forms_d[root_form] = current_form
    elif len(old_form) == len(current_form) and old_form[-1] == 'a':
      forms_d[root_form] = current_form

  as_id = data[i][0]
  dose = data[i][4]
  if (as_id, root_form, dose) not in substitute_groups:
    l += 1
    substitute_groups[(as_id, root_form, dose)] = (l, 0)
  sub_id, counter = substitute_groups[(as_id, root_form, dose)]
  counter += 1
  substitute_groups[(as_id, root_form, dose)] = (sub_id, counter)
  data[i][1] = sub_id


# W trzeciej iteracji uzupełniamy najdłuższą nazwę.

for i in range(len(data)):
  data[i][3] = forms_d[add_form(data[i][3])]


def more_stats():
  names = list(names_s)
  names.sort()
  forms_l = list(map(lambda form: forms_d[form[1]], forms))
  forms_l.sort()
  doses = list(doses_s)
  doses.sort()
  pd.DataFrame(names, columns=['name']).to_csv('names.csv')
  pd.DataFrame(forms_l, columns=['form']).to_csv('forms.csv')
  pd.DataFrame(doses, columns=['dose']).to_csv('doses.csv') 

  top_subs = list()
  for group in substitute_groups:
    id, counter = substitute_groups[group]
    as_id, form, dose = group
    top_subs.append((counter, active_substances_r[as_id], form, dose,))

  top_subs.sort()
  top_subs.reverse()


# Poniżej łączymy się z bazą danych i uzupełniamy dane początkowe.

from database.connection import connection, engine
from sqlalchemy import text, MetaData, insert


with connection() as con:
  with open("init_tables.sql") as file:
    query = text(file.read())
    con.execute(query)
  
meta = MetaData(bind=engine)
meta.reflect()
active_substances_t = meta.tables['active_substance']
ingredients = meta.tables['ingredient']
medicines = meta.tables['medicine']

with connection() as con:
  for as_name, as_id in active_substances.items():
    query = insert(active_substances_t).values(
      id=as_id, 
      name=as_name
    )
    con.execute(query)

  for group, id in substitute_groups.items():
    sub_id, _ = id
    as_id, sub_form, sub_dose = group
    query = insert(ingredients).values(
      id=sub_id, 
      form=sub_form, 
      dose=sub_dose, 
      active_substance=as_id
    )
    con.execute(query)

# data[i] = [as_id, 0, name, old_form, dose, quantity, med[4], med[12], med[14], med[15]]
# id | name | ingredient | quantity | id_code | refund_scope | refund | surcharge
  for i, med in enumerate(data):
    query = insert(medicines).values(
      id=(i + 1), 
      name=med[2], 
      ingredient=med[1], 
      quantity=med[5], 
      id_code=med[6], 
      refund_scope=med[7],
      refund=med[8],
      surcharge=med[9]
    )
    con.execute(query)
