from connectLDAP.connector import *
from automation.userful_functions import *
from datetime import date
from ldap3 import ObjectDef, Reader, ALL, MODIFY_ADD, LDIF, SYNC, MODIFY_DELETE
from automation.ldfi_wirte_funcitons import *
import random
import string

strs = "Christian JOVELIN christian.jovelin@arcelormittal.com".split(" ")
print(strs)
mail = strs[2]
premon = strs[0]
nom = strs[1]
nom = nom.upper()
app = "reiwa"

uid = "ARC00008"

# Stratégie LDAP3, LDIF print juste le ldif dans output.ldif, SYNC effectue la modif dans le ldap
strategy = LDIF

Env = {'PROD': {"app": "APPL_" + app, "conn": Connector().prod_ext(),"c_add": Connector(client_strategy=strategy).prod_ext()}}
env = "PROD"

conn = Env[env]["conn"]
mon_app = Env[env]["app"]


# Check si le mail existe
if conn.search('ou=users,o=ext.wallonie.be', '(&(mail='+mail+')(!(ou:dn:=XXX_TO_DELETE)))', attributes=['*']):
    print("email in use!!")
    print(conn.entries)
    uid = conn.entries[0]["uid"][0]
    dn_user = conn.entries[0].entry_dn
# Si il existe pas, sort les gens ac la même fin de mail
else :
    conn.search('o=ext.wallonie.be', '(mail=' + "*@" + mail.split("@")[1] + ')', attributes=['uid', 'mail'])
    print(conn.entries)
    conn.search('o=ext.wallonie.be', '(uid=' + uid[:3] + '*)', attributes=['uid', 'mail'])
    print(conn.entries)
    dn_user = "uid="+uid +","+ conn.entries[0].entry_dn.split(",",1)[1]

if conn.search('o=ext.wallonie.be', '(&(cn='+mon_app+')(ou:dn:=groups))', attributes=['*']):
    dn_app = conn.entries[0].entry_dn
else:
    print("Pas de dn trouvé")
    exit(-1)



def get_random_string(length):
    # choose from all lowercase letter
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


c = Env[env]["c_add"]
c.bind()
if strategy == LDIF:
    f = open("ldif/" + mon_app+ env + date.today().strftime("%Y-%m-%d")+nom+premon + ".ldif", "w")
else:
    exit(-1)

f.write('#add pour '  +nom + " " +premon + '\r')
dn_out = dn_user.replace("o=ext.wallonie.be","dc=external,dc=ovd")
c.modify(dn_app,{'uniqueMember': [(MODIFY_ADD, [dn_out])]})
write_ldif(c,strategy,f)

f.write('#create user pour '  +nom + " " +premon + '\r')
c.add(dn_user, ['top','organizationalPerson', 'person', 'inetOrgPerson'], {'cn': str(nom + " " + premon), 'sn': nom,"givenname": premon,"mail":mail,"uid":uid,"userpassword":get_random_string(16) })
write_ldif(c,strategy,f)

# close the connection
c.unbind()
f.close()