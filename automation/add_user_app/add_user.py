from connectLDAP.connector import *
from automation.userful_functions import *
from datetime import date
from ldap3 import ObjectDef, Reader, ALL, MODIFY_ADD, LDIF, SYNC, MODIFY_DELETE
from automation.ldfi_wirte_funcitons import *
import random
import string

strs = """51412
37634
47231
53415
53513
40476""".split("\n")

app = "securiwal"


# Stratégie LDAP3, LDIF print juste le ldif dans output.ldif, SYNC effectue la modif dans le ldap
strategy = LDIF

Env = {'PROD': {"app": "APPL_" + app, "conn": Connector().prod_ext(),"c_add": Connector(client_strategy=strategy).prod_ext()}}
env = "PROD"

conn = Env[env]["conn"]
mon_app = Env[env]["app"]

if conn.search('o=ext.wallonie.be', '(&(cn='+mon_app+')(ou:dn:=groups))', attributes=['*']):
    dn_app = conn.entries[0].entry_dn

c = Env[env]["c_add"]
c.bind()
if strategy == LDIF:
    f = open("ldif/" + mon_app+ env + date.today().strftime("%Y-%m-%d")+ ".ldif", "w")
else:
    exit(-1)
dn_list = []
for user in strs:
    dn_list.append("uid="+user+",ou=users,dc=internal,dc=ovd")

f.write('#add pour '  +app+ '\r')
c.modify(dn_app,{'uniqueMember': [(MODIFY_ADD, dn_list)]})
write_ldif(c,strategy,f)

# close the connection
c.unbind()
f.close()