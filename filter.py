import pandas as pd
import re 

#def filter(df):
df = pd.read_excel('source_data.xlsx', sheet_name='A1', usecols=[0,1,3], skiprows=1)


# '500 ml/g/mg'
regex = "^(\d+|\d+,\d+) (ml|g|mg)$"
# '1 ampułko-strzykawka/.../tabletka/wstrzykiwacz'
regex += "|^\d+ (ampułko-strzykawka|dawka|fiolka|implant|kapsułka|pojemnik|saszetka|tabletka|wstrzykiwacz|szt|sztuka|butelka|wkład) *$"

# '1 inhalator/pojemnik/butelka 60 dawka/sztuka'                
regex += "|^\d+ (inhalator|pojemnik|butelka) +\d+ (dawka|sztuka) *$"
# '1 saszetka/wstrzykawka/wstrzykiwacz/ampułko-strzykawka/.../fiolka 5 ml/g/mg'                TO NIE                       czy wstrzykawka i wsztrzykiwacz to to samo?
regex += "|^\d+ (butelka|saszetka|wstrzykawka|wstrzykiwacz|ampułko-strzykawka|ampułka|wkład|pojemnik|fiolka|worek|tuba) +(\d+|\d+,\d+) (ml|g|mg)$"


#random:

# '50 sztuka (5 blister 10 sztuka)'
regex += "|^\d+ sztuka +\(\d+ blister +\d+ sztuka +\)$"


#TAKIE JESZCZE DO PRZEJRZENIA:

# '1 fiolka proszku + 1 ampułko-strzykawka rozp.'       
regex += "|^\d+ fiolka +proszku \+ \d+ ampułko-strzykawka +rozp\.$"

# '1 zestaw (tacki)'                
regex += "|^\d+ zestaw +\(tacki\)$"
# '500 ml (butelka)'
regex += "|^(\d+|\d+,\d+) ml \(butelka *\)$"
# '500 sztuka (butelka)'
regex += "|^\d+ sztuka +\(butelka *\)$"
# '500 sztuka (w pojemniku)'
regex += "|^\d+ sztuka +\(w pojemniku\)$"
# '500 tabletka (butelka)'
regex += "|^\d+ tabletka *\(butelka *\)$"
# '50 sztuka (blister)'
regex += "|^\d+ sztuka +\(blister *\)$"


count = 0

def rozpisz(zaw):
    zaw = zaw.replace("fiol.", "fiolka ")
    zaw = zaw.replace("szt..", "sztuka ").replace("szt.", "sztuka ")
    zaw = zaw.replace("daw.", "dawka ").replace("dawek", "dawka")
    zaw = zaw.replace("amp.-", "ampułko-").replace("amp.", "ampułka ")
    zaw = zaw.replace("kaps.", "kapsułka ")
    zaw = zaw.replace("wkł.", "wkład ").replace("wkladów", "wkład")
    zaw = zaw.replace("poj.", "pojemnik ")
    zaw = zaw.replace("sasz.", "saszetka ")
    zaw = zaw.replace("wstrzykiwaczy", "wstrzykiwacz")
    zaw = zaw.replace("tabl.", "tabletka ").replace("tabletki", "tabletka")
    zaw = zaw.replace("strz.", "strzykawka ").replace("strzyk.", "strzykawka ")
    zaw = zaw.replace("but.", "butelka ").replace("butelki", "butelka").replace("butelek", "butelka")
    zaw = zaw.replace("inh.", "inhalator ")
    zaw = zaw.replace("zest.", "zestaw ")
    zaw = zaw.replace("blist.", "blister ")
    zaw = zaw.replace(" a ", " ").replace(" po ", " ").replace(" o ", " ")
    zaw = zaw.replace("  ", " ")
    return zaw
df["Zawartość opakowania"] = df["Zawartość opakowania"].apply(rozpisz)

for index,row in df.iterrows():
    if not ( bool(re.search(regex, row["Zawartość opakowania"])) )  :
        print(row.to_string(header=None))
        count += 1

print("Znaleziono niepasujących: ", count)

