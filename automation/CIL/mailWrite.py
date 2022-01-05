import webbrowser
import os
from connectLDAP.connector import Connector
import pandas as pd
from csv_import import *
import collections
Auteur_du_mail = "Jérôme Dewandre"

groupe_fonctionnel = 'CIL'

connector = Connector()
conn = connector.prod_mrw()


def produce_column(l):
    st = """"""
    for p in l:
        st = st + p + """<br aria-hidden="true">""" + "\n"
    return st


def get_attribut(genre):
    attribut = ""
    if genre == 'F':
        attribut = "Madame "
    elif genre == 'M':
        attribut = "Monsieur "
    return attribut


tbl_html = ""
ES_dn = collections.OrderedDict(sorted(ES_dn.items()))
for ES in ES_dn:
    print(ES)
    personnes = list(ES_dn[ES].members[groupe_fonctionnel]['personnes'])
    before_html = produce_column(personnes)
    personnes_after = personnes.copy()
    Nom_ES = ES_dn[ES].Nom_ES

    # check s'il y a des deletion
    if bool(ES_dn[ES].modif["deletion"]):
        for k, v in ES_dn[ES].modif["deletion"].items():
            print(v)
            genre = v["mrw-attr-sexe"].values[0]
            name = v.cn.values[0]
            _name = v.personnes.values[0]
            personne_attribut = get_attribut(genre)
            found = False
            for i in range(len(personnes_after)):

                if _name == personnes_after[i]:
                    found = True
                    personnes_after[i] = """<span style="background-color:yellow;"><s>""" + personnes_after[
                        i] + """</s></span>"""
                else :
                    print(_name + "  " + personnes_after[i])
            # Si la personne à supprimer n'est pas trouvée dans l'ES print le
            if not found:
                print(personne_attribut + _name + " n'a pas été trouvé(e) dans l'ES " + ES)

    # check s'il y a des ajout
    if bool(ES_dn[ES].modif["ajout"]):
        for k, v in ES_dn[ES].modif["ajout"].items():
            genre = v["mrw-attr-sexe"].values[0]
            name = v.cn.values[0]
            _name = v.personnes.values[0]
            personne_attribut = get_attribut(genre)
            personnes_after.append("""<span style="background-color:yellow;">""" + _name + """</span">""")

    after_html = produce_column(personnes_after)

    tbl_html = tbl_html + """<tr>
<td valign="top" style="width:110.45pt;padding:0 5.4pt;border-width:1pt;border-style:none solid solid solid;border-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;"> """ + ES + """</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
<td valign="top" style="width:110.45pt;padding:0 5.4pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:black;border-bottom-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;">""" + Nom_ES + """</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
<td valign="top" style="width:118.3pt;padding:0 5.4pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:black;border-bottom-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;">&nbsp;
""" + before_html + """
</span></p>
</td>
<td valign="top" style="width:118.3pt;padding:0 5.4pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:black;border-bottom-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt">&nbsp;
""" + after_html + """
</span>
</p></td>
</tr>"""

    verbe = ""
    if True:
        verbe0 = "a été enlevé(e)"
        verbe1 = "a bien été enlevé"

    # Si c'est un ajout, ajoute la personne
    else:
        verbe0 = " est créé(e)"
        verbe1 = " a bien été créé"

# Hide -a sentense if CI
phrase_a = 'hidden'
if groupe_fonctionnel == 'CI':
    phrase_a = """<p  style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;">Les modifications sont en ordre dans l’annuaire.</span>
    </p>"""
elif groupe_fonctionnel == 'CIL':
    phrase_a = """<p  style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;">Le compte -a de """ + name + verbe1 + """ et les modifications sont en ordre dans l’annuaire.</span>
    </p>"""

body = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
    h1   {color: blue;}
    p    {font-size:11pt;font-family:Calibri,sans-serif;}
</style>
</head>
<body>
<div>
<p style="margin:0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;">Bonjour,</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;font-family:Arial,sans-serif;"></span></p>
<p style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;">Suite à la demande ci-dessous, les changements suivants ont été effectués dans l’entité suivante :&nbsp;</span></p>
<p style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;">&nbsp;</span></p>
<div class_object="ugHd8hEKTmP3zNa_t33nm" style="width: 100%;" has-hovered="true"><div class_object="_3OSvA877av7sNgMphVnY6Z"><button type="button" class_object="ms-Button ms-Button--icon KBwACy35vUu44VLeJybtU root-225" title="Afficher la taille d’origine" aria-label="Afficher la taille d’origine" data-is-focusable="true"><span class_object="ms-Button-flexContainer flexContainer-162" data-automationid="splitbuttonprimary"><i data-icon-name="FullScreen" aria-hidden="true" class_object="ms-Icon root-89 css-157 ms-Button-icon icon-164" style="font-family: controlIcons;"></i></span></button></div>
<table border="1" cellspacing="0" cellpadding="0" style="border-collapse: collapse; border-style: none; transform-origin: left top;" >
<tbody>
<tr>
<td valign="top" style="width:110.45pt;padding:0 5.4pt;border:1pt solid black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;">CODE ES</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
<td valign="top" style="width:110.45pt;padding:0 5.4pt;border-width:1pt;border-style:solid solid solid none;border-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;">Nom de l'ES</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
<td valign="top" style="width:118.3pt;padding:0 5.4pt;border-width:1pt;border-style:solid solid solid none;border-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;">Liste des """ + groupe_fonctionnel + """ <span data-markjs="true" class_object="markkkybhap5w" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="" style="background-color: rgb(255, 241, 0); color: black;"></span> AVANT&nbsp;MODIFICATION</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
<td valign="top" style="width:110.45pt;padding:0 5.4pt;border-width:1pt;border-style:solid solid solid none;border-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;">Liste des """ + groupe_fonctionnel + """ <span data-markjs="true" class_object="markkkybhap5w" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="" style="background-color: rgb(255, 241, 0); color: black;"></span> APRES MODIFICATION</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
</tr>
""" + tbl_html + """
</tbody>
</table></div>
<p style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;font-family:Arial,sans-serif;">&nbsp;</span></p>
<p style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;">""" + personne_attribut + name + """</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"> """ + verbe0 + """ comme """ + groupe_fonctionnel + """ <span data-markjs="true" class_object="markkkybhap5w" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="" style="background-color: rgb(255, 241, 0); color: black;"></span> de l’entité </span><span style="color:#172B4D;font-size:11.5pt;">""" + ES + """</span><span style="color:#172B4D;font-size:11.5pt;">.</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
""" + phrase_a + """   
<p style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;">Pourriez-vous faire de même dans les applications concernées par ces changements s’il-vous-plait ?</span></p>
<p style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;">Bonne journée,</span></p>
<p style="margin:0;" aria-hidden="true">&nbsp;</p>
<p style="margin:0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;">""" + Auteur_du_mail + """</span></p>
</div>
</body>
</html>"""

html = body
path = os.path.abspath('temp.html')
url = 'file://' + path

with open(path, 'w', encoding="utf8") as f:
    f.write(html)
webbrowser.open(url)
