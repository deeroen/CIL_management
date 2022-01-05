from connectLDAP.connector import Connector
from ldap3 import ObjectDef, Reader, ALL, MODIFY_ADD, LDIF, SYNC, MODIFY_DELETE
import collections
from csv_import import *
from datetime import date


def clean_LDIF(input):
    return input.replace('\r\n ', '').replace('version: 1\r\n', '').replace('\n', '')


def write_ldif(c):
    if strategy == LDIF:
        f.write(clean_LDIF(c.response))
    else:
        pass
        # f.write(str(c.result))
    f.write('\r\n')


ES_dn = collections.OrderedDict(sorted(ES_dn.items()))

# Stratégie LDAP3, LDIF print juste le ldif dans output.ldif, SYNC effectue la modif dans le ldap
strategy = LDIF
# Connecteur pour la création de LDIF
connector = Connector(client_strategy=strategy)
c = connector.prod_mrw()
c.bind()

if strategy == LDIF:
    f = open("data/" + str(date.today()) + groupe_fonctionnel + ".ldif", "w")
else:
    exit(-1)

for ES in ES_dn:
    print(ES)
    dn = ES_dn[ES].dn
    path = groupe_cn + ',' + dn
    # check s'il y a des deletions
    f.write('#modif pour ' + dn + '\r')
    if bool(ES_dn[ES].modif["deletion"]):

        for k, v in ES_dn[ES].modif["deletion"].items():
            member = "uid=" + k + ",ou=users,o=mrw.wallonie.be"

            c.modify(path,
                     {'uniqueMember': [(MODIFY_DELETE, [member])]})
            write_ldif(c)

    # check s'il y a des ajout
    if bool(ES_dn[ES].modif["ajout"]):
        for k, v in ES_dn[ES].modif["ajout"].items():
            member = "uid=" + k + ",ou=users,o=mrw.wallonie.be"
            c.modify(path,
                     {'uniqueMember': [(MODIFY_ADD, [member])]})
            write_ldif(c)

# close the connection
c.unbind()

f.close()
