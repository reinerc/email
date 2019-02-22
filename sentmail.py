#
# Sent an email
#
# Copy-pasted from 
# https://stackoverflow.com/questions/6270782/how-to-send-an-email-with-python
#

import smtplib
import json


conffile = "test.json"
f=open(conffile,"rt")
dat = json.load(f)
import getpass


SERVER=dat["smtpserver"]
server = smtplib.SMTP(SERVER)
server.starttls()
LOGIN=dat["serverlogin"]
p=getpass.getpass()
FROM = dat["from"]
TO = dat["to"]
SUBJECT = dat["subject"]
TEXT = dat["text"]

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM,TO, SUBJECT, TEXT)

server.login(LOGIN,p)

server.sendmail(FROM, TO, message)
#or with a copy to me:
#server.sendmail(FROM, [TO,FROM], message)

server.quit()
