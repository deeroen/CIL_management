from connectLDAP.connector import *
from automation.userful_functions import *
from datetime import date


attributes = ['uid', 'cn', 'mrw-attr-sexe', 'uid', 'cn', 'sn', 'givenName', 'mail']
connector = Connector()
conn = connector.valid_ext()

'''Cherche tous les utilisateur de l'app en question'''
conn.search('ou=users,o=mrw.wallonie.be', '(&(uid=AL*)(businessCategory=S1*))', attributes=['*'])
print(len(conn.entries))

