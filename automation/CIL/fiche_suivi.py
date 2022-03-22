import pandas as pd
from connectLDAP.connector import *
from automation.CIL.class_object.Classes import *
from datetime import date

#df = pd.read_excel("C:/Users/AL7871/Downloads/Modification CIL SPW F.xlsx")
ajout = pd.read_csv("data/ajout.csv")
deletion = pd.read_csv("data/deletion.csv")


#out = pd.DataFrame(columns=deletion.columns).drop("Unnamed: 0", axis=1)

out = pd.concat([ajout,deletion],ignore_index=True).drop("Unnamed: 0", axis=1)
conn = Connector().prod_mrw()
es_list = out['identifiant ES'].unique().tolist()
conn.search('ou=business structure,o=mrw.wallonie.be', uidList_to_filter(es_list), attributes=['*'])

ES_dn = {}
for i in conn.entries:
    ES_id = i.entry_dn.split("=")[1].split(',')[0]
    print(ES_id)
    ES_dn[ES_id] = ES(ES_id, conn)
    print(i.entry_dn)

out.insert(3, "modif", "")
out.insert(0, "pris en charge par", "Jérôme Dewandre")

out.insert(0, "date de la demande", str(date.today()))
out["Libellé ES"] = ""
out["date"] = str(date.today())
fill = []
for index, row in out.iterrows():
    fill.append(ES_dn[row['identifiant ES']].Nom_ES)
out["Libellé ES"] = fill
out.insert(2, "DG", "V")
print(out)
out
out.to_excel("data/out.xlsx", index=False)
