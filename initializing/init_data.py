import pandas as pd

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
forms_s = set()
doses_s = set()

for (i, med) in enumerate(raw_data):
  match = re.search('\d,\d', med[2])
  while match:
    idx = match.start() + 1
    med[2] = med[2][:idx] + '.' + med[2][idx + 1:]
    match = re.match('\d,\d', med[2])

  sth = med[2].split(',')
  name = sth[0]
  form = ''
  dose = ''

  for (j, form_trait) in enumerate(sth[1:]):
    if re.match('.*\d.*', form_trait):
      form = ','.join(sth[1:j + 1])
      dose = ','.join(sth[j + 1:])
      break

  while form[0] == ' ':
    form = form[1:]
  
  while dose[0] == ' ':
    dose = dose[1:]

  if med[1] not in active_substances:
    k += 1
    active_substances[med[1]] = k

  as_id = active_substances[med[1]]

  if (as_id, form, dose) not in substitute_groups:
    l += 1
    substitute_groups[(as_id, form, dose)] = l

  sub_id = substitute_groups[(as_id, form, dose)]
  
  data[i] = np.array([as_id, sub_id, name, form, dose, med[3], med[4], med[12], med[14], med[15]])
  names_s.add(name)
  forms_s.add(form)
  doses_s.add(dose)

names = list(names_s)
names.sort()
forms = list(forms_s)
forms.sort()
doses = list(doses_s)
doses.sort()
pd.DataFrame(names, columns=['name']).to_csv('names.csv')
pd.DataFrame(forms, columns=['form']).to_csv('forms.csv')
pd.DataFrame(doses, columns=['dose']).to_csv('doses.csv')
