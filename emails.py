"""
Simple email program, that checks for
unread messages on the server
"""

import sys
from getpass import getpass
import json
import logging

logger = logging.getLogger('email_client')
logger.setLevel(logging.INFO)

from email.header import decode_header
import imapclient

logging.basicConfig(level=logging.WARN)

# module email is not compatible between different versions
# of Python 3.x, so it is not used anymore in this program
# import email
# from email.parser import Parser

#
# Individual Parameters to configure
#

host = "imap.web.de"
user = "rczerwi@web.de"
p = None
folders = None

conffile = None

if len(sys.argv) > 1:
  conffile = sys.argv[1]

if conffile:
   f = open(conffile,"tr")
   dat = json.load(f)
else:
   dat={"imapserver" : "imap.web.de","account": "rczerwi@web.de"}

host = dat.get("imapserver",host)
user = dat.get("account",user)
p = dat.get("password",None)
folders = dat.get("folders",None) # list of folders to scan, by default, the 
                                  # program go into every folder
nofolders= dat.get("no_folders",[]) # list of folders not to scan

# if _short is True, print further information (from, subject)
# of unread mails
_short = False


###########################################################


def search_uids(imapserver, folders, searchopt=["UNSEEN"]):
    hh = {}
    for fold in folders:
        imapserver.select_folder(fold, readonly=True)
        uids = serv.search(searchopt)
        if uids != []: hh[fold] = uids
    return hh


def get_messages(server, folder, uids, readonly=True):
    server.select_folder(folder, readonly=readonly)
    a = server.fetch(uids, ['BODY[]'])
    messages = {}
    for m in a.keys():
        #     messages[m]=Parser().parsestr(a[m][b'BODY[]'])
        messages[m] = a[m][b'BODY[]']
    return messages


def get_messagetag(message, tag='Subject:'):
    """
    Search in a string or bytestream for lines
    beginning with the parameter tag (default:'Subject:')
    """
    return list(filter(lambda x: x.startswith(tag), message.strip().decode('utf-8', errors='replace').splitlines()))


serv = imapclient.IMAPClient(host, ssl=True)

if not(p):
  p = getpass(prompt="Email password:")

serv.login(user, p)

if not(folders):
  l = serv.list_folders()
  logger.debug(l)
#h = search_uids(serv, filter(lambda x: x != 'Postausgang', map(lambda x: x[2], filter(lambda x: len(x[0]) == 1, l))))
  folders = list(filter(lambda x: x != 'Postausgang', map(lambda x: x[2], filter(lambda x: len(x[0]) == 1, l))))
logger.debug("Folders :{}".format(folders))
logger.debug("Don't used Folders:{}".format(nofolders))
folders = list(set(folders).difference(nofolders))
logger.info("Folders :{}".format(folders))
h = search_uids(serv, folders)
#print(list(folders))

logging.debug(h)

if _short:
    print(h)
    sys.exit(0)

m = {}
for k in h.keys():
    m = get_messages(serv, k, h[k])
    print("Folder :" + k)
    for message in m.keys():
        print(get_messagetag(m[message], 'From:'), decode_header(get_messagetag(m[message])[0]))

# serv.logout()
