import sys
sys.path.append('../')
from database.authentication import *
from sqlalchemy import create_engine

engine = create_engine('postgresql://' + db_user + ':' + db_pass + '@' + db_host + ':5432/' + db_name)

def connection():
  global engine
  return engine.connect()

# Funkcja debugująca, wypisuje na konsolę zawartość tabeli o nazwie name.
def print_table(name):
  with connection() as con:
    rs = con.execute('select * from ' + name)
    for row in rs:
      print(row)