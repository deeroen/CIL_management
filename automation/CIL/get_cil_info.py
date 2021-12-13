from connectLDAP.connector import *
import pandas as pd
from datetime import date
from automation.userful_functions import *
import time
import subprocess
uid = "AL7871978"
ES = "A1000000"


def tiret_a_existe(uid):
    """Cette fonction check le resulat  de 'net user <uid>-a /domain et stop le programme si l'user
    n'as pas de -a"""
    # filters output
    try :
        subprocess.check_output('net user ' + uid + '-a /domain')
        print("Le conte -a existe")
    except :
            print("Le conte -a n'existe pas")
            return exit(-1)
    return 0

tiret_a_existe(uid)

connector = Connector()
conn = connector.dev_mrw()

conn.search('o=mrw.wallonie.be', '(&(ou:dn:=business structure)(uid=' + ES + '))', attributes=['*'])

print(conn.entries)
print(conn.entries[0].entry_attributes_as_dict)
ES_name = conn.entries[0].entry_attributes_as_dict['cn'][0]
uid_request = get_uid_from_uniqueMember(conn.entries[0])


attributs=['cn','uid','businessCategory','mrw-attr-sexe']
conn.search('o=mrw.wallonie.be', uid_request, attributes=attributs)

df = search_to_df(attributs,conn)
df['Nom_ES'] = ES_name
print(df)