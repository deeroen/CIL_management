from connectLDAP.connector import *
from automation.userful_functions import *
from datetime import date
from ldap3 import ObjectDef, Reader, ALL, MODIFY_ADD, LDIF, SYNC, MODIFY_DELETE
from automation.ldfi_wirte_funcitons import *
df = pd.read_excel("C:/Users/AL7871/Downloads/PEGA-ACM-AES2.xlsx")
df['Identifiant'] = df['Identifiant'].astype(str).str.replace("\\u200b", "", regex=True).str.lower()
df['path'] = [
    "uid=" + i + ",ou=users,dc=internal,dc=ovd" if "acm_" not in i else "uid=" + i + ",ou=demo_users,dc=external,dc=ovd"
    for i in df['Identifiant']]

# Stratégie LDAP3, LDIF print juste le ldif dans output.ldif, SYNC effectue la modif dans le ldap
strategy = LDIF

Env = {'DEV': {"app": "pega-acmdev", "conn": Connector().dev_ext(),"c_add": Connector(client_strategy=strategy).dev_ext()},
       'TEST': {"app": "pega-acmtest", "conn": Connector().test_ext(),"c_add": Connector(client_strategy=strategy).test_ext()},
       'VALID': {"app": "pega-acm", "conn": Connector().valid_ext(),"c_add": Connector(client_strategy=strategy).valid_ext()},
       'PROD': {"app": "APPL_pega-acm", "conn": Connector().prod_ext(),"c_add": Connector(client_strategy=strategy).prod_ext()}}

for env in Env:

    df[env] = df[env].notna()

    mon_app = Env[env]["app"]

    # attributes = ['uid', 'cn', 'internationaliSDNNumber', 'mrw-attr-sexe', 'uid', 'cn', 'sn', 'givenName', 'mail']
    attributes = ['uid', 'cn', 'mrw-attr-sexe', 'uid', 'cn', 'sn', 'givenName', 'mail']

    conn = Env[env]["conn"]

    '''Cherche tous les utilisateur de l'app en question'''
    conn.search('o=ext.wallonie.be', '(cn=' + mon_app + ')', attributes=['cn', 'description', 'uniqueMember'])
    print(conn.entries)

    # Crée la requête pour la branche mrw
    raw_list = []
    for i in conn.entries:
        '''Ici je selectionne l'applicaiton qui m'intéresse'''
        if i.entry_attributes_as_dict['cn'] == [mon_app]:
            raw_list = i
    Env[env]["dn"] = raw_list.entry_dn

    uid_request = get_uid_filter_from_uniqueMember(raw_list)
    print(raw_list.entry_attributes_as_dict['uniqueMember'])
    out = pd.DataFrame({"ladap"+env: True,'path': raw_list.entry_attributes_as_dict['uniqueMember']})
    out['path'] = out['path'].str.lower()

    final = out.set_index('path').join(df[[env,'Identifiant','path']].set_index('path'), how='outer', lsuffix='_caller', rsuffix='_other')

    # Ajoute les utilisateurs de la liste fournie qui n'y sont pas et retir les utilisateur de la liste qui ne doivent pas y être
    final["add"] = (final[env] == True).values & (final["ladap"+env] !=True).values
    final["remove"] = (final[env] == False).values & (final["ladap"+env] ==True).values
    final['path'] = final.index


    """
    ldap + ENV = présence de la personne dans le ldap (vrai: il est présent, rien: il n'est pas présent), ENV = la demande de la personne (vrai: il faut ajouter, Faux: il ne doit pas être présent, rien: ne fait pas partie de la demande)
    add: faut il ajouter la personne
    remove: faut il l'enlever?
    path, le path à ajouter en fonction de l'identifiant
    
    """
    final.to_excel("data/" + mon_app+env + str(date.today()) + '.xlsx',index=False)



for env in Env:
    mon_app = Env[env]["app"]
    c = Env[env]["c_add"]
    c.bind()

    if strategy == LDIF:
        f = open("ldif/" + mon_app+env + str(date.today()) + ".ldif", "w")
    else:
        exit(-1)
    xlsx = pd.read_excel("data/" + mon_app + env + str(date.today()) + '.xlsx')

    for index,row in xlsx.iterrows():
        if row['add']:
            print(row['path'])
            # check s'il y a des deletions
            f.write('#add pour ' + row['Identifiant'] + '\r')

            c.modify(Env[env]["dn"],
                         {'uniqueMember': [(MODIFY_ADD, [row['path']])]})

            write_ldif(c,strategy,f)

        if row['remove']:
            print(row['path'])
            # check s'il y a des deletions
            f.write('#remove pour ' + row['Identifiant'] + '\r')

            c.modify(Env[env]["dn"],
                         {'uniqueMember': [(MODIFY_DELETE, [row['path']])]})
            write_ldif(c,strategy,f)

    # close the connection
    c.unbind()

    f.close()