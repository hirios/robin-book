import os
import ast
import smtplib
import argparse
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders



with open('config.txt') as f:
	config = ast.literal_eval(f.read())


parser = argparse.ArgumentParser()
parser.add_argument('--email', help='set your email')
parser.add_argument('--bookname', help='set bookname')
args = parser.parse_args()

EMAIL_ADDRESS = config["email"]
EMAIL_PASSWORD = config["app_password"]

msg = MIMEMultipart()
msg['Subject'] = 'Convert'
msg['From'] = EMAIL_ADDRESS
msg['To'] = args.email


if os.path.isfile(os.path.join("AZW3", args.bookname.replace('.epub', '.mobi'))):
	PATH = os.path.join("AZW3", args.bookname.replace('.epub', '.mobi'))
	bookname = args.bookname.replace('.epub', '.mobi')
else:
	PATH = os.path.join("EPUB", args.bookname)
	bookname = args.bookname

with open(PATH,'rb') as f:
    file_data = f.read()
    file_name = bookname


#mobi = MIMEApplication(file_data)
#mobi.add_header('Content-Disposition', 'attachment', name=file_name, filename=file_name)
#msg.attach(mobi)


part = MIMEBase("application", "octet-stream")
part.set_payload(open(PATH, "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', name=file_name, filename=file_name)
msg.attach(part)


#msg.add_attachment(file_data, maintype="application", subtype='octet-stream', filename=file_name)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()
    print('<--- EMAIL ENVIADO COM SUCESSO --->')
