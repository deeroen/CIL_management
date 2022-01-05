import pandas as pd

ajout = pd.read_csv("automation/CIL/data/ajout.csv")
deletion = pd.read_csv("automation/CIL/data/deletion.csv")

out = pd.concat([ajout.reset_index(drop=True), deletion.reset_index(drop=True) ], axis=0)

out.insert(0, "pris en charge par", "Jérôme")
out.insert(0, "date de la demande", "04/01/22")
out["Libellé ES"] = ""
out["date"]="05/01/22"
for index, row in out.iterrows():
    out["Libellé ES"][index]=ES_dn[row['identifiant ES']].Nom_ES
out.to_excel("automation/CIL/data/out.csv")


