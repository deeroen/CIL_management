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

uid_request = get_uid_filter_from_uniqueMember(raw_list)