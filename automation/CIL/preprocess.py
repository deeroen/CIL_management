import pandas as pd
from connectLDAP.connector import *
from automation.CIL.class_object.Classes import *

groupe_fonctionnel = 'CI'

conn = Connector().prod_mrw()
es = ["O7000000"]
conn.search('ou=business structure,o=mrw.wallonie.be', uidList_to_filter(es), attributes=['*'])

ES_dn = {}
for i in conn.entries:
    ES_id = i.entry_dn.split("=")[1].split(',')[0]
    print(ES_id)
    ES_dn[ES_id] = ES(ES_id, conn)
    print(i.entry_dn)



ajout = ["135143","56643","126935"]
deletion = ["134095"]
modifs = Modification(ajout+deletion,conn)
# ajoute dans le champ modif de chaque objet ES, les ajouts et les deletions
for i in ES_dn:
    for row in deletion:
        ES_dn[i].modif["deletion"][row] = modifs.df[modifs.df['uid'] == row]
    for row in ajout:
        ES_dn[i].modif["ajout"][row]= modifs.df[modifs.df['uid'] == row]
