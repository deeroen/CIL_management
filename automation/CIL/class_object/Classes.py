from ldap3 import ObjectDef, Reader
from automation.userful_functions import *





class ES():
    def __init__(self, es_id, conneciton):
        self.es_id = es_id
        self.conn = conneciton
        self.dn, self.Nom_ES = self.get_dn(self.conn)
        self.a = False
        self.members = self.get_OLD_members(self.conn)
        self.modif = {"ajout":{},"deletion":{}}

    def get_dn(self, conn):
        # Retrouve le dn de l'ES et son nom complet
        conn.search('o=mrw.wallonie.be', '(&(ou:dn:=business structure)(uid=' + self.es_id + '))', attributes=['*'])

        if len(conn.entries) != 1:
            print(
                "Error: Plusieur ou aucun ES trouvés pour " + self.es_id + " , le paramètre 'groupe_fonctionnel' est il bien configuré?")
            print(conn.entries)
            exit(-1)

        dn = conn.entries[0].entry_dn
        Nom_ES = conn.entries[0]['cn'][0]

        return dn, Nom_ES

    def get_OLD_members(self, conn):
        # Retrouve les CIL(CI) de l'ES
        groupe_fonctionnel_dict = {'CIL': '(cn=Correspondant informatique local CIL)',
                                   'CI': '(cn=Coordinateur informatique CI)'}
        out = {'CIL': "", 'CI': ""}
        for key in groupe_fonctionnel_dict:
            conn.search(self.dn, groupe_fonctionnel_dict[key], search_scope='LEVEL', attributes=['*'])
            if len(conn.entries) != 1:
                out[key] = {
                    "Error: Plusieur ou aucun groupe fonctionnels trouvés comme " + key + " de " + self.es_id: conn.entries}
            else:
                ## Retrouve l'uid des CILS de l'ES
                uid_request = get_uid_filter_from_uniqueMember(conn.entries[0])
                out[key] = get_genre_df(conn, uid_request)
        return out


class Modification():
    """
    Cette classe prend en argument une liste de uid et une connection
    df contient un dataframe avec chaque ligne contenant un cil modifié
    """
    def __init__(self, uids, conn):
        self.uids = uids
        self.conn = conn
        self.df = self.get_cil_info()
        self.ALL_a_existe = self.tiret_a()


    def get_cil_info(self):
        """
        Retrouve toutes les infos (genre,...) des CIL de l'ES à partir d'un filtre contenant tous leurs uid (uid_request)
        :return: un dataframe
        """
        uid_request = uidList_to_filter(self.uids)
        df = get_genre_df(self.conn, uid_request)
        return df

    def tiret_a(self):
        """
        Retourne un dictionnaire donnant pour chaque uid, si le -a existe
        :return:
        """
        dic = {}
        ALL_existe = True
        for i in self.uids:
            dic[i] = tiret_a_existe(i)
            if not dic[i]:
                ALL_existe = False
        self.ALL_a_existe = ALL_existe
        return dic
#from connectLDAP.connector import Connector
#a = ES("O7000000",Connector().prod_mrw())
#hey=1