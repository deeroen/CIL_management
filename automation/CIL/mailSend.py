import win32com.client as win32
import os
from mailWrite import body
outlook = win32.Dispatch('outlook.application')
inbox = outlook.GetNamespace("MAPI").GetDefaultFolder(6)
#for i in inbox.Items:
#    if i.Subject =='Changements CIL':
#        mail = i.Reply()
mail = outlook.CreateItem(0)
mail.To = 'jerome.dewandre.ext@spw.wallonie.be;jerome.dewandre.ext@spw.wallonie.be'
mail.Subject = 'Changements CIL'
mail.Body = 'Changements CILS'
mail.HTMLBody = body #this field is optional

mail.saveas(os.getcwd()+"\\cil.msg")
#mail.Send()

print("Email envoyé")