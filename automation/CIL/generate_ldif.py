from connectLDAP.connector import Connector
from ldap3 import ObjectDef, Reader, ALL, MODIFY_ADD, LDIF, SYNC, MODIFY_DELETE
import collections
from csv_import import *
from datetime import date
from automation.ldfi_wirte_funcitons import *



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
    path = ES_dn[ES].groupe_fonctionnel_dict[groupe_fonctionnel].split("(")[1].split(")")[0] + ',' + dn
    print(path)
    # check s'il y a des deletions
    f.write('#modif pour ' + dn + '\r')
    if bool(ES_dn[ES].modif["deletion"]):
        for k, v in ES_dn[ES].modif["deletion"].items():
            member = "uid=" + k + ",ou=users,o=mrw.wallonie.be"
            c.modify(path,
                     {'uniqueMember': [(MODIFY_DELETE, [member])]})
            write_ldif(c,strategy,f)

    # check s'il y a des ajout
    if bool(ES_dn[ES].modif["ajout"]):
        for k, v in ES_dn[ES].modif["ajout"].items():
            member = "uid=" + k + ",ou=users,o=mrw.wallonie.be"
            c.modify(path,
                     {'uniqueMember': [(MODIFY_ADD, [member])]})
            write_ldif(c,strategy,f)

# close the connection
c.unbind()

f.close()
