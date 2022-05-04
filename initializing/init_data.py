import pandas as pd

def remove_white_chars(text):
  p = 0
  q = len(text) - 1

  while p <= q and text[p] == ' ':
    p += 1
  while p <= q and text[q] == ' ':
    q -= 1

  return text[p:q + 1]

data_frame = pd.read_excel('./init_data.xlsx', sheet_name='A1')
data_frame.to_csv('./init_data.csv', index = None, header=False, sep='|')

import numpy as np
import re 

raw_data = np.loadtxt("init_data.csv", skiprows = 1, delimiter = '|', dtype=str)
data = np.full((len(raw_data), 10), '')

active_substances = dict()
substitute_groups = dict()
k = 0
l = 0
names_s = set()
doses_s = set()
forms = list()

def add_form(new_form):
  global forms
  new_regex = new_form.replace('.', r'[a-ząćęńłśóżź]*\.?')
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
  form = add_form(remove_white_chars(form))

  if med[1] not in active_substances:
    k += 1
    active_substances[med[1]] = k
  as_id = active_substances[med[1]]

  if (as_id, form, dose) not in substitute_groups:
    l += 1
    substitute_groups[(as_id, form, dose)] = (l, 0)
  sub_id, counter = substitute_groups[(as_id, form, dose)]
  counter += 1
  substitute_groups[(as_id, form, dose)] = (sub_id, counter)

  data[i] = np.array([as_id, sub_id, name, form, dose, med[3], med[4], med[12], med[14], med[15]])
  names_s.add(name)
  doses_s.add(dose)

names = list(names_s)
names.sort()
forms_l = list(map(lambda form: form[1], forms))
forms_l.sort()
doses = list(doses_s)
doses.sort()
pd.DataFrame(names, columns=['name']).to_csv('names.csv')
pd.DataFrame(forms_l, columns=['form']).to_csv('forms.csv')
pd.DataFrame(doses, columns=['dose']).to_csv('doses.csv')
