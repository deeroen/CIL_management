from connectLDAP.connector import *

connector = Connector()
conn = connector.prod_mrw()

conn.search('ou=users,o=mrw.wallonie.be', '(ObjectClass=mrw-oc-acteurs)', attributes=['uid'])

len(conn.entries)

All_mrw = []
for i in conn.entries:
    All_mrw = All_mrw + [i["uid"].value.lower()]

# Drop duplicate
All_mrw = list(dict.fromkeys(All_mrw))
print("MRW: " + str(len(All_mrw)))
conn2 = connector.prod_ext()
conn2.search('o=ext.wallonie.be', '(|(cn=APPL_intranet)(cn=APPL_diagonales)(cn=wbi)(cn=ssg)(cn=ivcie)(cn=eap)(cn=APPL_rdp))', attributes=['uniqueMember'])

All_ext = []

for i in conn2.entries:
    All_ext = All_ext  + i["uniqueMember"].values
All_ext = [ z.split("=")[1].split(",")[0].lower() for z in All_ext]

# Drop duplicate
All_ext = list(dict.fromkeys(All_ext))
print(len(All_ext))
All_ext = [i for i in All_ext if (not i.isnumeric() and "al" not in i)]
print("EXT: " + str(len(All_ext)))

All = All_ext + All_mrw

All = list(dict.fromkeys(All))
print("ALL: " + str(len(All)))

# AL
len([i for i in All_mrw if (not i.isnumeric())])
# Ulis
len([i for i in All_mrw if (i.isnumeric())])