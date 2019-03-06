"""
Send an email
"""

import json
import smtplib
import getpass
import sys


conffile = "test.json"


if len(sys.argv) > 1:
  conffile = sys.argv[1]
  print(conffile)


f = open(conffile, "rt")

dat = json.loads(f.read().encode('utf-8').decode('utf-8','replace'))

#
# Get data from JSON File
#

SERVER = dat["smtpserver"]
server = smtplib.SMTP(SERVER)
server.starttls()
LOGIN = dat["serverlogin"]
p = getpass.getpass()
FROM = dat["from"]
FROM = "rczerwi@web.de"
TO = dat["to"]

#
# Optional Data
#
SUBJECT = dat.get("subject", "Test")
TEXT = dat.get("text", "")
TEXTFILE = dat.get("textfile", None)
APPENDFILE = dat.get("appendfile", None)

if TEXTFILE:
    f = open(TEXTFILE, "rt")
    text = f.read()
else:
    text = TEXT

if not APPENDFILE:

    #
    # Email without attachment
    #
    # Copy-pasted from
    # https://stackoverflow.com/questions/6270782/how-to-send-an-email-with-python
    #

    message = """From: %s
To: %s
Subject: %s

%s
  """ % (FROM, TO, SUBJECT, text)

else:
    #
    # Email with an attachment (PDF File)
    #
    #  needs Python 3.x
    #
    # Copy-pasted from
    # https://stackoverflow.com/questions/44388020/how-to-attach-a-pdf-file-to-a-mime-email-in-python
    #

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

    message = MIMEMultipart()
    message['Subject'] = SUBJECT
    message['From'] = FROM
    message['Reply-to'] = FROM
    message['To'] = TO

    text = MIMEText(TEXT)
    message.attach(text)

    # directory = "C:\ExamplePDF.pdf"
    with open(APPENDFILE, "rb") as opened:
        openedfile = opened.read()
    # attachedfile = MIMEApplication(openedfile, _subtype = "pdf", _encoder = encode_base64)
    attachedfile = MIMEApplication(openedfile, _subtype="pdf")
    attachedfile.add_header('content-disposition', 'attachment', filename=APPENDFILE)
    message.attach(attachedfile)

    # print("not implemeted")
    # sys.exit(1)
    message = message.as_string()

server.login(LOGIN, p)

print(message)
print(TO)
print(TEXTFILE)

server.sendmail(FROM, TO, message)
# or with a copy to me:
# server.sendmail(FROM, [TO,FROM], message)

server.quit()
