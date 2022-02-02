from connectLDAP.connector import *
from ldap3 import ObjectDef, Reader
from automation.userful_functions import *

connector = Connector()

txt = """AND00013"""

lst = txt.split("\n")
out = {}
conn = connector.prod_mrw()
obj_inetorgperson = ObjectDef('mrw-oc-groupesfonctionnels', conn)
r = Reader(conn, obj_inetorgperson, 'o=mrw.wallonie.be')
r.search()
for i in lst:
    out[i] = {}
    out[i]["mrw"] = []
    uid = "uid=" + i + ",ou=users,o=mrw.wallonie.be"

    list = []

    for entry in r.entries:
        for user in entry['uniqueMember']:
            if user.lower() == uid.lower():
                list.append(entry.entry_dn)
                # print(entry)
                out[i]["mrw"].append(entry.entry_dn)
                break
    print(list)


obj = ObjectDef('groupOfUniqueNames', conn)
r = Reader(conn, obj, 'o=ext.wallonie.be')
r.search()

for i in lst:
    out[i]["ext"] = []

    uid = get_uniqueMember(conn, i)

    print(txt.lower())
    list = []

    for entry in r.entries:
        for user in entry['uniqueMember']:

            if user.lower() == uid.lower():
                list.append(entry.entry_dn)
                # print(entry)
                out[i]["ext"].append(entry.entry_dn)
                break
    print(list)

print(out)

