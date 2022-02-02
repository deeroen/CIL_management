import pandas as pd
from connectLDAP.connector import *
from automation.CIL.class_object.Classes import *
from automation.userful_functions import *
groupe_fonctionnel = 'CIL'

df = pd.read_excel("C:/Users/AL7871/Downloads/CILS2.xlsx")

conn = Connector().prod_mrw()
conn.search('ou=business structure,o=mrw.wallonie.be', uidList_to_filter(df["identifiant ES"].values), attributes=['*'])

ES_dn = {}
for i in conn.entries:
    ES_id = i.entry_dn.split("=")[1].split(',')[0]
    print(ES_id)
    ES_dn[ES_id] = ES(ES_id, conn)
    print(i.entry_dn)


#df["Acrréditation retirées"] = df["Acrréditation retirées"].str.upper()
df["identifiant ES"] = df["identifiant ES"].str.replace(' ', '')
for index, row in df[df["identifiant ES"] == "EnsembledesES"].iterrows():
    for key in ES_dn:
        df = df.append({"NOM Prénom": row["NOM Prénom"], "ULIS ID": row["ULIS ID"], "Designation": row["Designation"],
                        "Acrréditation retirées": row["Acrréditation retirées"], "identifiant ES": key},
                       ignore_index=True)

df = df[df['identifiant ES'] != 'EnsembledesES'].reset_index(drop=True)


deletion = df[df["Designation"].isna()].reset_index(drop=True)
ajout = df[df["Acrréditation retirées"].isna()].reset_index(drop=True)

# Personne devant être rajoutées comme CIL
for index, row in ajout.iterrows():
    if all(str(row["ULIS ID"]) != ES_dn[row["identifiant ES"]].members[groupe_fonctionnel]["uid"]):
        print(str(row["ULIS ID"]) + "  " + row["identifiant ES"])
    else:
        ajout.drop(index, inplace=True)
for index, row in deletion.iterrows():
    if any(str(row["ULIS ID"]) == ES_dn[row["identifiant ES"]].members[groupe_fonctionnel]["uid"]):
        print(str(row["ULIS ID"]) + "  " + row["identifiant ES"])
    else:
        deletion.drop(index, inplace=True)


all_cils = list(set(list(ajout["ULIS ID"]) + list(deletion["ULIS ID"])))
modifs = Modification([str(i) for i in all_cils], conn)

# ajoute dans le champ modif de chaque objet ES, les ajouts et les deletions
for index, row in deletion.iterrows():
    ES_dn[row["identifiant ES"]].modif["deletion"][str(row["ULIS ID"])] = modifs.df[modifs.df['uid'] == str(row["ULIS ID"])]
for index, row in ajout.iterrows():
    ES_dn[row["identifiant ES"]].modif["ajout"][str(row["ULIS ID"])]= modifs.df[modifs.df['uid'] == str(row["ULIS ID"])]

ajout.to_csv("data/ajout.csv")
deletion.to_csv("data/deletion.csv")