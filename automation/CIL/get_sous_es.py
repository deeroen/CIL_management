from connectLDAP.connector import *
from ldap3 import ObjectDef, Reader

from automation.userful_functions import *
groupe_fonctionnel = 'CIL'

conn = Connector().prod_mrw()
conn.search('ou=business structure,o=mrw.wallonie.be', "(&(uid:dn:=S2000200)(ObjectClass=organizationalPerson))", attributes=['*'])

print(conn.entries)
out = []
for i in conn.entries:
    print(i.entry_dn)
    out.append(i.entry_dn)
list = [i.split(",")[0].split("=")[1] for i in out]
print(list)
