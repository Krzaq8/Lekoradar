from os import sep
import pandas as pd
import numpy as np
import re 
import sys
sys.path.append('../')


# Sprowadza tekst zawartości do prostszej formy. 
# Zamienia słowa kluczowe na 'X' jeśli wartości po obu stronach 'X' mają być przemnożone.
def normal_quantity_form(quantity):
  quantity = quantity.replace('(', '').replace(')', '')
  quantity = quantity.replace('. a', '.').replace('.a', '.').replace('. po', '.').replace('.po', '.')
  quantity = quantity\
    .replace('but.', 'X')\
    .replace('amp.', 'X')\
    .replace('butelka', 'X')\
    .replace('butelka po', 'X')\
    .replace('butelki', 'X')\
    .replace('butelki po', 'X')\
    .replace('x', 'X')\
    .replace('bliser', 'X')\
    .replace('fiol.', 'X')\
    .replace('inh.', 'X')\
    .replace('inhalator', 'X')\
    .replace('tuba', 'X')\
    .replace('poj.', 'X')\
    .replace('wstrzyk.', 'X')\
    .replace('wstrz. SoloStar po', 'X')\
    .replace('wstrz.', 'X')\
    .replace('wstrzykiwaczy', 'X')\
    .replace('worek po', 'X')
  return quantity


# Wyłuskuje pierwszą znalezioną liczbę rzeczywistą w tekscie.
def get_first_number(text):
  return float(list(re.findall(r'\d+[.,]?\d*', text))[0].replace(',', '.'))


# Zamienia w tekście przecinki oddzielające liczby na kropki.
def comas_to_dots_in_floats(text):
  match = re.search(r'\d,\d', text)
  while match:
    idx = match.start() + 1
    text = text[:idx] + '.' + text[idx + 1:]
    match = re.match(r'\d,\d', text)
  return text


# Wyznacza z tekstu nazwę, postać i dawkę leku.
def separate_name_form_dose(text):
  elements = comas_to_dots_in_floats(text).split(',')
  form = ''
  dose = ''

  for (j, form_trait) in enumerate(elements[1:]):
    if re.match(r'.*\d.*', form_trait):
      form = ','.join(elements[1:j + 1])
      dose = ','.join(elements[j + 1:])
      break

  return (elements[0], form.strip(), dose.strip())


# Zamienia tekst zawartości opakowania na wartość liczbową.
def get_quantity(quantity_string):
  parts = normal_quantity_form(quantity_string).split(' ')
  if len(parts) >= 3 and parts[1] == 'X':
    return float(parts[0]) * get_first_number(parts[2])
  else:
    return get_first_number(quantity_string)


# Poprawia tekst postaci, w której pozostały błędy po automatycznej obróbce.
def correct_final_form(form):
  return form\
    .replace('kaps.', 'kapsułki')\
    .replace('dojel.', 'dojelitowe')\
    .replace('amp.-strzyk..', 'ampułko-strzykawce')\
    .replace('tabl.', 'tabletki')\
    .replace('powl.', 'powlekane')\
    .replace('przedł.', 'przedłużonym')\
    .replace('kapsułce twardej', 'kapsułkach twardych')


data_frame = pd.read_excel('source_data.xlsx', sheet_name='A1')
data_frame.to_csv('tmp_data.csv', index = None, header=False, sep='|')

raw_data = np.loadtxt("tmp_data.csv", skiprows = 1, delimiter = '|', dtype=str)
data = [[] for _ in range(len(raw_data))]

active_substances = dict()
active_substances_r = dict()
substitute_groups = dict()
k = 0
l = 0
names_s = set()
doses_s = set()
forms = list()
forms_d = dict()


# Dodaje nową postać do zbioru.
# Dwie postacie są takie same jeśli jedną da się rozwinąć (skróty zakończone kropką) do drugiej.
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


# Dodaje substancję do zbioru. Zwraca jej id.
def add_substance(substance):
  global active_substances

  if substance not in active_substances:
    add_substance.counter += 1
    active_substances[substance] = add_substance.counter
    active_substances_r[add_substance.counter] = substance
  return active_substances[substance]

add_substance.counter = 0


# Pierwsza iteracja: zbieramy dane.
# Te których nie trzeba obrabiać od razu wrzucamy, resztę dodajemy do struktur.

for (i, med) in enumerate(raw_data):
  name, old_form, dose = separate_name_form_dose(med[2])

  form = add_form(old_form)

  as_id = add_substance(med[1])

  quantity = get_quantity(med[3])
  surcharge = get_first_number(med[15])

  data[i] = [as_id, 0, name, old_form, dose, quantity, med[4], med[12], med[14], surcharge, form]
  names_s.add(name)
  doses_s.add(dose)


# W drugiej iteracji znamy już najkrótsze napisy postaci.
# Dla każdej takiej szukamy jej najdłuższego odpowiednika.
# Ponadto możemy podzielić już na grupy odpowiedników.


for i in range(len(data)):
  current_form = data[i][3]
  root_form = data[i][10]
  
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
    substitute_groups[(as_id, root_form, dose)] = l
  sub_id = substitute_groups[(as_id, root_form, dose)]

  data[i][1] = sub_id


def more_stats():
  global names_s
  global forms_d
  global forms
  global doses_s
  names = list(names_s)
  names.sort()
  forms_l = list(map(lambda form: forms_d[form[1]], forms))
  forms_l.sort()
  doses = list(doses_s)
  doses.sort()
  pd.DataFrame(names, columns=['name']).to_csv('names.csv')
  pd.DataFrame(forms_l, columns=['form']).to_csv('forms.csv')
  pd.DataFrame(doses, columns=['dose']).to_csv('doses.csv') 


more_stats()

quit()

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

  for group, sub_id in substitute_groups.items():
    as_id, sub_form, sub_dose = group
    query = insert(ingredients).values(
      id=sub_id, 
      form=forms_d[sub_form], 
      dose=sub_dose, 
      active_substance=as_id
    )
    con.execute(query)

# data[i] = [as_id, sub_id, name, old_form, dose, quantity, med[4], med[12], med[14], med[15]]
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
