from connectLDAP.connector import *
import pandas as pd
from datetime import date
mon_app = 'APPL_bcedwi'
attributes = ['uid', 'cn', 'internationaliSDNNumber', 'mrw-attr-sexe', 'uid', 'cn', 'sn', 'givenName', 'mail']
connector = Connector()
conn = connector.prod_ext()

'''Cherche tous les utilisateur de l'app en question'''
conn.search('o=ext.wallonie.be', '(cn=*' + mon_app + '*)', attributes=['cn', 'description', 'uniqueMember'])
print(conn.entries)

# Crée la requête pour la branche mrw
raw_list = []
for i in conn.entries:
    '''Ici je selectionne l'applicaiton qui m'intéresse'''
    if i.entry_attributes_as_dict['cn'] == [mon_app]:
        raw_list = i.entry_attributes_as_dict['uniqueMember']
uid_list = ['(' + i.split(',')[0] + ')' for i in raw_list]
uid_request = '(|' + ''.join(uid_list) + ')'
print(uid_request)
'''Cherche dans la branche mrw tout les utilisateurs de l'app'''
conn.search('o=mrw.wallonie.be', uid_request, attributes=attributes)

#print(conn.entries)

'''Ecrit dans un excel avec le nom de l'app et la date'''
out = pd.DataFrame(columns=attributes)
for i in conn.entries:
    dict = i.entry_attributes_as_dict
    for key, value in dict.items():
        '''Si pas l'attribut n'existe pas, rajoute un string vide'''
        if not value == []:
            dict[key] = value[0]
        else:
            dict[key] = ""
    out = out.append(dict, ignore_index=True)
out.index += 1
out.to_excel(str(date.today()) + mon_app + ".xlsx")