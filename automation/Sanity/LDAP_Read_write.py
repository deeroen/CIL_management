"""Ce fichier est utilisé pour la migration des gestionnaire d'acteur dans tous les environnements"""
from connectLDAP.connector import Connector
from ldap3 import ObjectDef, Reader, ALL, MODIFY_ADD, LDIF, SYNC, MODIFY_REPLACE


def clean_LDIF(input):
    return input.replace('\r\n ', '').replace('version: 1\r\n', '').replace('\n', '')


# Stratégie LDAP3, LDIF print juste le ldif dans output.ldif, SYNC effectue la modif dans le ldap
strategy = SYNC
uid = "AL7871"

if strategy == LDIF:
    f = open("ldif_log/outldif", "w")
else:
    f = open("output.txt", "w")

# Connecteur pour la création de LDIF
lt = [Connector(client_strategy=strategy).dev_mrw, Connector(client_strategy=strategy).prod_mrw,
      Connector(client_strategy=strategy).test_mrw, Connector(client_strategy=strategy).valid_mrw]
for conn in lt:
    env = str(conn).split(" of")[0].split(".")[1]
    print(env)
    c = conn()
    c.bind()
    # perform the Modify operation
    c.modify('uid=' + uid + ',ou=users,o=mrw.wallonie.be',
             {'mrw-attr-sexe': [(MODIFY_REPLACE, ['F'])]})
    f.write('#Modifie le genre pour pour ' + env + '\r')
    if strategy == LDIF:
        f.write(clean_LDIF(c.response))
    else:
        f.write(str(c.result)+env)
    f.write('\r\n')
    c.modify('uid=AL7871,ou=users,o=mrw.wallonie.be',
             {'mrw-attr-sexe': [(MODIFY_REPLACE, ['M'])]})

    f.write('#Modifie le genre pour pour ' + env + '\r')
    if strategy == LDIF:
        f.write(clean_LDIF(c.response))
    else:
        f.write(str(c.result)+env)
    f.write('\r\n')
    c.unbind()
# close the connection


f.close()
