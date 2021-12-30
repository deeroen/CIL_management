from connectLDAP.connector import *
from ldap3 import ObjectDef, Reader

connector = Connector()

txt = """41236"""

lst = txt.split("\n")
out = {}
conn = connector.valid_mrw()
obj_inetorgperson = ObjectDef('mrw-oc-groupesfonctionnels', conn)
r = Reader(conn, obj_inetorgperson, 'o=mrw.wallonie.be')
r.search()
for i in lst:
    out[i] = {}
    out[i]["mrw"] = []
    uid = "uid="+i+",ou=users,o=mrw.wallonie.be"

    list = []

    for entry in r.entries:
        for user in entry['uniqueMember']:
            if user.lower() == uid.lower():
                list.append(entry.entry_dn)
                #print(entry)
                out[i]["mrw"].append(entry.entry_dn)
                break
    print(list)

conn = connector.prod_ext()
obj = ObjectDef('groupOfUniqueNames', conn)
r = Reader(conn, obj, 'o=ext.wallonie.be')
r.search()
for i in lst:
    out[i]["ext"] = []

    #Check if ulis, don't work with AL
    if i.isdecimal():
        uid = "uid=" + i + ",ou=users,o=mrw.wallonie.be"
        uid = uid.replace("o=mrw.wallonie.be", "dc=internal,dc=ovd")

    else:
        conn.search('o=ext.wallonie.be', "(uid="+i+")", attributes=["uid"])
        uid =conn.entries[0].entry_dn
    print(uid)
    list = []

    for entry in r.entries:
        for user in entry['uniqueMember']:

            if user.lower() == uid.lower():
                list.append(entry.entry_dn)
                #print(entry)
                out[i]["ext"].append(entry.entry_dn)
                break
    print(list)

print(out)