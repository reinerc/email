"""
Simple email program, that is checking for
unread emails on the server
"""

from getpass import getpass

import imapclient
import email
from email.parser import Parser

def search_uids(imapserver,folders,searchopt=["UNSEEN"]):
   hh={}
   for fold in folders:
       imapserver.select_folder(fold)
       uids=serv.search(searchopt)
       if uids!=[]:hh[fold]=uids
   return hh

def get_messages(server,folder,uids):
  server.select_folder(folder)
  a=server.fetch(uids,['BODY[]'])
  messages={}
  for m in a.keys():
     messages[m]=Parser().parsestr(a[m]['BODY[]'])
  return messages

def get_senders(messages):
    return list(set(map(lambda x:x['From'],messages.values())))

def store_attachements(msg,prefix=""):
# store the attachment of an email 
# the_email must have type email.message
   for part in msg.walk():
      if part.get_filename():
        f=open(prefix+ part.get_filename()+part.get_content_type().split("/")[1],"wb")
        f.write(part.get_payload(decode=True))
        f.close()

 
host="imap.web.de"
user="rczerwi@web.de"

serv=imapclient.IMAPClient(host,ssl=True)

p = getpass(prompt="Email password:")

serv.login(user,p)

l=serv.list_folders() 

h= search_uids(serv,filter(lambda x:x!='Postausgang',map(lambda x:x[2],filter(lambda x:len(x[0])==1 ,l))))
       
print(h)
#for fold in filter(lambda x:x!='Postausgang',map(lambda x:x[2],filter(lambda x:len(x[0])==1 ,l))):
#     print fold
#     serv.select_folder(fold)
#     print serv.search(["UNSEEN"])


#serv.logout()
