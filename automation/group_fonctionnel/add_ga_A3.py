"""Ce fichier est utilisé pour la migration des gestionnaire d'acteur dans tous les environnements"""
from connectLDAP.connector import Connector
from ldap3 import ObjectDef, Reader, ALL, MODIFY_ADD, LDIF,SYNC

def clean_LDIF(input):
    return input.replace('\r\n ', '').replace('version: 1\r\n', '').replace('\n','')


lt = ['uid=A30000001,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000100,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000200,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000200A,uid=A3000200,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000300,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000400,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000500,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000600,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000700,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000700A,uid=A3000700,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000700A1,uid=A3000700,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000700B,uid=A3000700,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000700C,uid=A3000700,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000700D,uid=A3000700,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000800,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3000900,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3001000,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3001100,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3001200,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3001300,uid=A3000000,ou=business structure,o=mrw.wallonie.be', 'uid=A3001400,uid=A3000000,ou=business structure,o=mrw.wallonie.be']


#Stratégie LDAP3, LDIF print juste le ldif dans output.ldif, SYNC effectue la modif dans le ldap
strategy =LDIF
#Connecteur pour la création de LDIF
connector = Connector(client_strategy=strategy)
c = connector.dev_mrw()
c.bind()
# Check si le groupe existe
c_verif = Connector().dev_mrw()

if strategy==LDIF:
    f = open("ldif_log/def.ldif","w")
else:
    f = open("output.txt","w")

for dn in lt:
    path = 'cn=Gestionnaire des acteurs,' + dn

    c_verif.search(path, "(cn=Gestionnaire des acteurs)", attributes=["*"])
    nb_GA = len(c_verif.entries)

    if nb_GA == 0:
        # perform the Add operation

        c.add(path,
              attributes={'objectClass': ['mrw-oc-groupesfonctionnels', 'groupOfUniqueNames', 'top'],
                          'cn': 'Gestionnaire des acteurs',
                          'uniqueMember': ['uid=127606,ou=users,o=mrw.wallonie.be',
                                           'uid=35474,ou=users,o=mrw.wallonie.be']})

        f.write('#Cree le groupe gestionnaire d acteurs pour '+dn+'\r')
        if strategy == LDIF:
            f.write(clean_LDIF(c.response))
        else :
            f.write(str(c.result))
        f.write('\r\n')

    else:
        print("GA existe pour " + path)
    # Check que le path n'a pas déjà été ajouté
    c_verif.search("ou=functions,o=mrw.wallonie.be", "(cn=Gestionnaire des acteurs)",
                   attributes=["mrw-attr-gf-refs"])
    found = False
    for i in c_verif.entries[0]["mrw-attr-gf-refs"]:
        if i == path:
            found = True
            break
    if not found:
        f.write('#Modifie pointeur pour ' + dn + '\r')
        c.modify("cn=Gestionnaire des acteurs,ou=functions,o=mrw.wallonie.be",
                 {'mrw-attr-gf-refs': [(MODIFY_ADD, [path])]})
        if strategy == LDIF:
            f.write(clean_LDIF(c.response))
        else:
            f.write(str(c.result))
        f.write('\r\n')
    else:
        print("Pointeur existe pour " + path)

# close the connection
c.unbind()

f.close()
