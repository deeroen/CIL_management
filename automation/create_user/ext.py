from connectLDAP.connector import *
from automation.userful_functions import *
from datetime import date
from ldap3 import ObjectDef, Reader, ALL, MODIFY_ADD, LDIF, SYNC, MODIFY_DELETE
from automation.ldfi_wirte_funcitons import *
import random
import string

strs = "Delphine	WAUDOIT	delphine.waudoit@cpas-villerslaville.be".split("\t")
print(strs)
mail = strs[2].lower()
premon = strs[0]
nom = strs[1]
nom = nom.upper()
app = "edocsdgt2"


# Stratégie LDAP3, LDIF print juste le ldif dans output.ldif, SYNC effectue la modif dans le ldap
strategy = LDIF

Env = {'PROD': {"app": "APPL_" + app, "conn": Connector().prod_ext(),"c_add": Connector(client_strategy=strategy).prod_ext()}}
env = "PROD"

conn = Env[env]["conn"]
mon_app = Env[env]["app"]


# Program to find most frequent
# element in a list
def most_frequent(List):
    return max(set(List), key = List.count)

def get_trigram(conn):
    entries = conn.entries
    filt_ATE = [entry["uid"][-1][:3] for entry in entries if entry["uid"][-1][:3] != "ATE"]
    if len(filt_ATE) == 0:
        return "DIV"
    else :
        return most_frequent(filt_ATE)

def get_updated_trigram(trigram):
    conn.search('o=ext.wallonie.be', '(uid=' + trigram + '*)', attributes=['uid', 'mail'])
    entries = conn.entries
    last_entry = entries[-1]
    mails = [(entry.uid,entry.mail) for entry in conn.entries]
    print(mails)
    entry_id = last_entry["uid"][-1]
    return entry_id[:3] + str(format(int(entry_id[3:]) + 1, '05d')), last_entry

def get_new_dn(conn,mail):
    conn.search('o=ext.wallonie.be', '(mail=' + "*@" + mail.split("@")[1] + ')', attributes=['uid', 'mail'])
    if len(conn.entries) == 0:
        print("This type of email was never used")
        uid, last_entry = get_updated_trigram("DIV")
    else:
        trigram = get_trigram(conn)
        print("Selected trigram +" + trigram)
        uid, last_entry = get_updated_trigram(trigram)
        print("uid " + uid)
        print(last_entry)
    return "uid=" + uid + "," + last_entry.entry_dn.split(",", 1)[1], uid
# Check si le mail existe
if conn.search('ou=users,o=ext.wallonie.be', '(&(mail='+mail+')(!(ou:dn:=XXX_TO_DELETE)))', attributes=['*']):
    print("email in use!!")
    print(conn.entries)
    if len(conn.entries) == 1 and conn.entries[0]["uid"][-1][:3] != "ATE":
        print("Non ATE account exist => EXIT program")
        exit(0)
    print("Generate new LDIF")
    dn_user, uid = get_new_dn(conn,mail)

# Si il existe pas, sort les gens ac la même fin de mail
else :
    dn_user, uid = get_new_dn(conn,mail)

if app == "":
    print("Pas d'app spécifiée")
elif conn.search('o=ext.wallonie.be', '(&(cn='+mon_app+')(ou:dn:=groups))', attributes=['*']):
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

if app != "":
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