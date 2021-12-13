import pandas as pd

def dict_unwrap(dict):
    """
    Cette fonction est faite pour palier au problème de ldap3 qui quand il crée un dict, englobe
    ses variables dans une liste []
    :param dict:
    :return:
    """
    for key, value in dict.items():
        '''Si pas l'attribut n'existe pas, rajoute un string vide'''
        if not value == []:
            dict[key] = value[0]
        else:
            dict[key] = ""
    return dict

def get_uid_from_uniqueMember(raw):
    """
    Cette fonction prend un objet contenant des valeur unique Member et retourne une liste de uid
    qui peut être utilisée comme filtre
    :param raw:
    :return:
    """
    raw = raw.entry_attributes_as_dict['uniqueMember']
    uid_list = ['(' + i.split(',')[0] + ')' for i in raw]
    return '(|' + ''.join(uid_list) + ')'

def search_to_df(attrib,connection):
    """
    Cette fonction prend en argument une connection sur laquelle une recherche a été faite
    et retourne un dataframe bien propre avec une ligne par personne/élément
    :param attrib: [] liste d'attribut ex: ['cn','uid',]
    :param connection:
    :return:
    """
    out = pd.DataFrame(columns=attrib)
    for i in connection.entries:
        dictionnaire = i.entry_attributes_as_dict
        dictionnaire = dict_unwrap(dictionnaire)
        out = out.append(dictionnaire, ignore_index=True)
    return out