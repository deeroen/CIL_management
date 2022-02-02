from connectLDAP.connector import *
import pandas as pd
from datetime import date
from automation.userful_functions import *
mon_app = 'APPL_bcedwi'
attributes = ['uid', 'cn', 'internationaliSDNNumber', 'mrw-attr-sexe', 'uid', 'cn', 'sn', 'givenName', 'mail']
connector = Connector()
conn = connector.prod_ext()

'''Cherche tous les utilisateur de l'app en question'''
conn.search('o=ext.wallonie.be', '(cn=' + mon_app + ')', attributes=['cn', 'description', 'uniqueMember'])
print(conn.entries)

# Crée la requête pour la branche mrw
raw_list = []
for i in conn.entries:
    '''Ici je selectionne l'applicaiton qui m'intéresse'''
    if i.entry_attributes_as_dict['cn'] == [mon_app]:
        raw_list = i



def al_to_df(lt,attrib,c):
    """Cette fonction prend en argument une liste d'AL (|(AL57)(..)..), une liste d'attributs et une connection pour renvoyer
    un dataframe contenant les attributs des AL"""
    c.search('o=mrw.wallonie.be',lt,attributes=attrib)
    print(conn.entries)

    data = []
    for i in conn.entries:
        data.append([i["uid"], i["sn"], i["givenName"], i["mail"], i["internationaliSDNNumber"]])

    return pd.DataFrame(data, columns=['uid', 'Nom', 'prénom', 'mail','internationaliSDNNumber'])
uid_request = get_uid_filter_from_uniqueMember(raw_list)
conn = connector.prod_mrw()
al_to_df(uid_request ,attributes,conn).to_excel("data/" + mon_app + str(date.today()) + "_groupe_applicatif"+ '.xlsx',index=False)

conn.search('ou=es libres,o=mrw.wallonie.be','(cn=*' + mon_app.split("_")[1].split("w")[0] + '*)',attributes=["*"])
uid_request = get_uid_filter_from_uniqueMember(conn.entries[0])
al_to_df(uid_request ,attributes,conn).to_excel("data/" + mon_app + str(date.today()) + "_ESlibre"+ '.xlsx',index=False)