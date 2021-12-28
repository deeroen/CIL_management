from connectLDAP.connector import Connector
from ldap3 import ObjectDef, Reader
connector = Connector()
conn = connector.test_mrw()

lt = []

obj_inetorgperson = ObjectDef(['mrw-oc-directions'], conn)
r = Reader(conn, obj_inetorgperson, 'ou=business structure,o=mrw.wallonie.be','uid:=*A3*')
r.search()

print(len(r.entries))
for e in r.entries:
    print(e.entry_dn.split(",")[0])
    lt.append(e.entry_dn)

obj_inetorgperson = ObjectDef(['mrw-oc-services'], conn)
r = Reader(conn, obj_inetorgperson, 'ou=business structure,o=mrw.wallonie.be','uid:=A3*')
r.search()
print(len(r.entries))
for e in r.entries:
    print(e.entry_dn.split(",")[0])
    lt.append(e.entry_dn)
lt.sort()
print(lt)
print(len(lt))