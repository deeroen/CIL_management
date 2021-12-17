from connectLDAP.connector import *
from automation.userful_functions import *


def get_cil_info(conn, ES, uid, groupe_fonctionnel):
    attributs = ['cn', 'uid', 'businessCategory', 'mrw-attr-sexe']
    if not tiret_a_existe(uid):
        return exit(-1)

    # This part must be changed to be loopable on multiple users with adds and removes
    def cn_from_uid(connection, user_id, att):
        connection.search('o=mrw.wallonie.be', '(uid=' + user_id + ')', attributes=att)
        return connection.entries[0]['cn'][0]

    def get_cn_uid(connection, user_id, att):
        return user_id + ' - ' + cn_from_uid(connection, user_id, att)

    def sexe_from_uid(connection, user_id, att):
        connection.search('o=mrw.wallonie.be', '(uid=' + user_id + ')', attributes=att)
        return connection.entries[0]['mrw-attr-sexe'][0]

    user_modif = [get_cn_uid(conn, uid, attributs)]

    genre = sexe_from_uid(conn, uid, attributs)

    # Retrouve le dn de l'ES et son nom complet
    conn.search('o=mrw.wallonie.be', '(&(ou:dn:=business structure)(uid=' + ES + '))', attributes=['*'])

    if len(conn.entries) != 1:
        print("Error: Plusieur ES trouvés")
        exit(-1)

    dn = conn.entries[0].entry_dn

    Nom_ES = conn.entries[0]['cn'][0]

    # Retrouve les CIL(CI) de l'ES
    groupe_fonctionnel_dict = {'CIL': '(cn=Correspondant informatique local CIL)', 'CI': '(cn=Coordinateur informatique CI)'}

    conn.search(dn, groupe_fonctionnel_dict[groupe_fonctionnel], search_scope='LEVEL', attributes=['*'])
    if len(conn.entries) != 1:
        print(conn.entries)
        print("Error: Plusieur groupe fonctionnels trouvés")
        exit(-1)
    ## Retrouve l'uid des CILS de l'ES
    uid_request = get_uid_from_uniqueMember(conn.entries[0])

    # Retrouve toutes les infos des CIL de l'ES à partir d'un filtre contenant tous leurs uid (uid_request)
    conn.search('o=mrw.wallonie.be', uid_request, attributes=attributs)
    df = search_to_df(attributs, conn)
    personnes = list(df[['uid', 'cn']].agg(' - '.join, axis=1))

    return personnes, Nom_ES, user_modif, genre
