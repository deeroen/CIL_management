from connectLDAP.connector import *
from automation.userful_functions import *
from datetime import date
from ldap3 import ObjectDef, Reader, ALL, MODIFY_ADD, LDIF, SYNC, MODIFY_DELETE, BASE
from automation.ldfi_wirte_funcitons import *


# Stratégie LDAP3, LDIF print juste le ldif dans output.ldif, SYNC effectue la modif dans le ldap
strategy = LDIF
ES = "O7070300"
Env = {'PROD': {"conn": Connector().prod_mrw(),"c_add": Connector(client_strategy=strategy).prod_mrw()}}
env = "PROD"

conn = Env[env]["conn"]

conn.search('o=mrw.wallonie.be', '(&(cn=Gestionnaire des acteurs)(uid:dn:='+ES+'))', attributes=['*'])
GA_list = conn.entries[0].uniqueMember.values
for GA in GA_list:
    conn.search(search_base=[GA],search_filter= '(objectClass=*)',search_scope=BASE, attributes=['mail','cn','uid'])
    print(conn.entries[0].mail,conn.entries[0].cn,conn.entries[0].uid)