from connectLDAP.connector import Connector
import re


al = """
dn:uid=AL7974,ou=users,o=mrw.wallonie.be
dn:uid=AL7975,ou=users,o=mrw.wallonie.be
dn:uid=AL7976,ou=users,o=mrw.wallonie.be
dn:uid=AL7977,ou=users,o=mrw.wallonie.be
dn:uid=AL7978,ou=users,o=mrw.wallonie.be
"""

al = al.split('\n')
al = list(filter(None, al))
str = "(|"
for i in al:
    str = str + "(" + re.split(":|,", i)[1] + ")"

filter_LDAP = str + ")"

connector = Connector()

def check_entries(conn, filter, list):
    conn.search('o=mrw.wallonie.be', filter, attributes=["uid"])
    return len(conn.entries) == len(list)

"""Valid"""
print("AL intégrés en valid= ")
print(check_entries(connector.valid_mrw(), filter_LDAP, al))

"""Test"""
print("AL intégrés en test= ")
print(check_entries(connector.test_mrw(), filter_LDAP, al))
