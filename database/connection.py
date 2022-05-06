from authentication import *
from sqlalchemy import create_engine

engine = create_engine('postgresql://' + db_user + ':' + db_pass + '@' + db_host + ':5432/' + db_name)
