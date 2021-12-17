from connectLDAP.connector import *
from automation.userful_functions import *
from ldap3 import ObjectDef,Reader

connector = Connector()
conn = connector.dev_mrw()
uid = 'uid=46969,ou=users,o=mrw.wallonie.be'
obj_inetorgperson = ObjectDef('groupOfUniqueNames', conn)
r = Reader(conn, obj_inetorgperson, 'o=mrw.wallonie.be','cn:=Correspondant informatique local CIL')
print(r)
r.search()
list = []

for entry in r.entries:
    for user in entry['uniqueMember']:
        if user == uid:
            list.append(entry.entry_dn)
            break
print(list)
list = [i.split(",")[1].split("=")[1]for i in list]
print(list)
