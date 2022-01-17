from connectLDAP.connector import *

connector = Connector()
conn = connector.prod_mrw()

conn.search('ou=buildings,o=mrw.wallonie.be', '(ObjectClass=mrw-oc-etage)', attributes=['cn', 'description', 'uniqueMember'])

dict = {}
for entry in conn.entries:
    dn = entry.entry_dn
    description = entry['description']
    mb_list = entry['uniqueMember']
    for mb in mb_list:
        if mb in dict.keys():
            print("Key exists for " + mb)
            dict[mb].append(description[0])
        else:
            dict[mb]=[]
            dict[mb].append(description[0])
out = {}
for k,v in dict.items():
    if len(v)>1:
        out[k.split("=")[1].split(",")[0]] = v
print(out)