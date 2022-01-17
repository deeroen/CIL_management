"""Ce fichier sert à retrouver les ES d'un cil pour une demande de suppression incomplète"""
from connectLDAP.connector import *
from ldap3 import ObjectDef, Reader

connector = Connector()
conn = connector.prod_mrw()
uid = 'uid=123296,ou=users,o=mrw.wallonie.be'
obj_inetorgperson = ObjectDef('groupOfUniqueNames', conn)
r = Reader(conn, obj_inetorgperson, 'o=mrw.wallonie.be','cn:=Correspondant informatique local CIL')
r.search()

list = []

for entry in r.entries:
    for user in entry['uniqueMember']:
        if user == uid:
            list.append(entry.entry_dn)
            break
print(list)
list = [i.split(",")[0].split("=")[1] for i in list]
print(list)


