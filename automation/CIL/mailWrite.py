import webbrowser
import os

ajout = True
Auteur_du_mail = "Jérôme Dewandre"
modif = ["150106 - HANAPPE Thérèse"]
ES = "O7000"


Nom_ES = "Service extérieur Eupen"
personnes = ["151162 - BARZIN François", "150106 - HANAPPE Thérèse", "42424 - DEBECQ Christopher",
             "40845 - DUSAUCOIT Jean-Christophe", "150068 - DELATTRE Cédric", "40179 - LEMPEREUR Benoit",
             "52238 - DENIS Sébastien", "37623 - PECHON Vincent", "53133 - TONGLET Nicolas"]

genre = "F"

name = []
for i in range(len(modif)):
    name.append(modif[i].split(" - ")[1])
name=name[0]


def produce_column(l):
    st = """"""
    for p in l:
        st = st + p + """<br aria-hidden="true">""" + "\n"
    return st


before_html = produce_column(personnes)

# Si c'est pas un ajout, barre la personne
verbe = ""
if not ajout:
    verbe0 = "a été enlevé(e)"
    verbe1 = "a bien été enlevé"
    for m in modif:
        for i in range(len(personnes)):
            if m == personnes[i]:
                personnes[i] = """<span style="background-color:yellow;"><s>""" + personnes[i] + """</s></span>"""


# Si c'est un ajout, ajoute la personne
else:
    verbe0 = "est créé(e)"
    verbe1 = "a bien été créé"
    for m in modif:
        personnes.append("""<span style="background-color:yellow;">""" + m + """</span">""")
after_html = produce_column(personnes)

personne_attribut = ""
if genre == 'F':
    personne_attribut = "Madame "
elif genre == 'M':
    personne_attribut = "Monsieur "

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
<div class="ugHd8hEKTmP3zNa_t33nm" style="width: 100%;" has-hovered="true"><div class="_3OSvA877av7sNgMphVnY6Z"><button type="button" class="ms-Button ms-Button--icon KBwACy35vUu44VLeJybtU root-225" title="Afficher la taille d’origine" aria-label="Afficher la taille d’origine" data-is-focusable="true"><span class="ms-Button-flexContainer flexContainer-162" data-automationid="splitbuttonprimary"><i data-icon-name="FullScreen" aria-hidden="true" class="ms-Icon root-89 css-157 ms-Button-icon icon-164" style="font-family: controlIcons;"></i></span></button></div>
<table border="1" cellspacing="0" cellpadding="0" style="border-collapse: collapse; border-style: none; transform-origin: left top;" >
<tbody><tr>
<td valign="top" style="width:110.45pt;padding:0 5.4pt;border:1pt solid black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;">CODE ES</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
<td valign="top" style="width:110.45pt;padding:0 5.4pt;border-width:1pt;border-style:solid solid solid none;border-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;">Nom de l'ES</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
<td valign="top" style="width:118.3pt;padding:0 5.4pt;border-width:1pt;border-style:solid solid solid none;border-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;">Liste des CIL <span data-markjs="true" class="markkkybhap5w" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="" style="background-color: rgb(255, 241, 0); color: black;"></span> AVANT&nbsp;MODIFICATION</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
<td valign="top" style="width:110.45pt;padding:0 5.4pt;border-width:1pt;border-style:solid solid solid none;border-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;">Liste des CIL <span data-markjs="true" class="markkkybhap5w" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="" style="background-color: rgb(255, 241, 0); color: black;"></span> APRES MODIFICATION</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
</tr>
<tr>
<td valign="top" style="width:110.45pt;padding:0 5.4pt;border-width:1pt;border-style:none solid solid solid;border-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;background-color:yellow;"> """ + ES + """</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
</td>
<td valign="top" style="width:110.45pt;padding:0 5.4pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:black;border-bottom-color:black;">
<p style="margin:7.5pt 0 0 0;"><span style="color:#172B4D;font-size:11.5pt;background-color:yellow;">""" + Nom_ES + """</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
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
</tr>
</tbody></table></div>
<p style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;font-family:Arial,sans-serif;">&nbsp;</span></p>
<p style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;background-color:yellow;">"""+ personne_attribut + name + """</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"> """ + verbe0 + """ comme CIL <span data-markjs="true" class="markkkybhap5w" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="" style="background-color: rgb(255, 241, 0); color: black;"></span> de l’entité </span><span style="color:#172B4D;font-size:11.5pt;background-color:yellow;">""" + ES + """</span><span style="color:#172B4D;font-size:11.5pt;">.</span><span lang="fr" style="color:#172B4D;font-size:11.5pt;"></span></p>
<p style="margin:7.5pt 0 0 0;"><span lang="fr" style="color:#172B4D;font-size:11.5pt;">Le compte -a de <span data-markjs="true" class="markkkybhap5w" data-ogac="" data-ogab="" data-ogsc="" data-ogsb=""
                        style="background-color: rgb(255, 241, 0); color: black;">""" + name + """</span> """ + verbe1 + """ et les modifications sont en ordre dans l’annuaire.</span></span>
    </p>
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
