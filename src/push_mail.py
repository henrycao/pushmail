#!/usr/bin/env python 
#coding:utf-8

import os, sys, time,getopt
import ConfigParser
import base64
import smtplib, email
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE, formatdate

vFILE=os.getcwd()+'/push_mail.conf'
if not os.path.exists(vFILE):
       	print 'where is the configure file!(push_mail.conf)'
       	sys.exit(-1)

parameterlen=len(sys.argv)
mail_file_path=''
if parameterlen<=1:
	print "usage:push_mail.py [Subject] [From Addr] [To Addr List (Comma-separated)] [Text] <File Path>"
	sys.exit(-1)
elif parameterlen==6:
	subject=sys.argv[1]
	from_addr=sys.argv[2]
	to_addr=sys.argv[3].split(',')
	text=sys.argv[4]
	try:
		mail_file_path=sys.argv[5]
	except Exception:
		pass
else:
	subject=sys.argv[1]
	from_addr=sys.argv[2]
	to_addr=sys.argv[3].split(',')
	text=sys.argv[4]

vCF=ConfigParser.ConfigParser()
vCF.read(vFILE)
smtp_server=vCF.get("mail","smtp_server")
username=vCF.get("mail","username")
password=vCF.get("mail","passwd")
mail_charset=vCF.get("mail","mail_charset")
mail_subtype=vCF.get("mail","mail_subtype")

from_addr = "<"+from_addr +">"
to_addr = to_addr

main_msg = email.MIMEMultipart.MIMEMultipart()
main_msg['From'] = from_addr
main_msg['To'] = COMMASPACE.join(to_addr)
main_msg['Subject'] = subject
text_msg = email.MIMEText.MIMEText(text, _subtype=mail_subtype, _charset=mail_charset)
main_msg.attach(text_msg)

if mail_file_path:
        contype = 'application/octet-stream'
	maintype, subtype = contype.split('/', 1)
	file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
	data = open(mail_file_path, 'rb')
	file_msg.set_payload(data.read())
	data.close()
	email.Encoders.encode_base64(file_msg)
	basename = os.path.basename(mail_file_path)
	file_msg.add_header('Content-Disposition', 'attachment',filename=basename)
	main_msg.attach(file_msg)
else:
	pass

main_msg['Date'] = email.Utils.formatdate()
fullText = main_msg.as_string()
svr=smtplib.SMTP(smtp_server)
svr.set_debuglevel(1)
svr.docmd("EHLO server")
svr.docmd("AUTH LOGIN")
svr.send(base64.encodestring(username))
svr.getreply()
svr.send(base64.encodestring(password))
svr.getreply()


try:
	svr.sendmail(from_addr, to_addr, fullText)
finally:
	svr.quit()
	print "Data has been successfully sent to: %s" %  to_addr
