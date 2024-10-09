import imaplib
import re
from config import *
import email
import smtplib
from email.mime.text import MIMEText



class mailobj:
	def __init__(self):
		self.username=""
		self.useremail=""
		self.subject=""
		self.body=""
		self.attachment=""
	def parsemail(self,mailObj):
		msg=email.message_from_bytes(mailObj)
		fromuser=msg['From']
		subject=msg['Subject']
		for part in msg.walk():
			if part.get_content_type() == 'text/plain' and part.get_content_disposition() is None:
				body = part.get_payload(decode=True).decode(part.get_content_charset())
			elif part.get_content_disposition() == 'attachment':
				self.attachment = part.get_payload(decode=True)
				self.filename = part.get_filename()
		self.useremail=re.search(r'<([^>]+)>',fromuser).group(1)
		self.username=re.search(r'^([^<]+)',fromuser).group(1)
		self.body=body
		self.subject=subject
		if self.registerComplaint():
			self.create_reply()
	def create_reply(self):
		smtp_host = 'mail.nullbyte.exe'
		smtp_user = ADMIN_CRED['username']
		smtp_pass = ADMIN_CRED['password']
		body="Your Request for "+self.subject+""" has been added to Issue and our team is actively working on it.
			
Best Regards,
IT Team
		"""
		msg = MIMEText(body)
		msg['Subject'] = "Ticket Created Sucessfully"
		msg['From'] = smtp_user
		msg['To'] = self.useremail
		try:
			with smtplib.SMTP_SSL('mail.nullbyte.exe',465) as server:
				server.login(smtp_user,smtp_pass)
				print(smtp_pass,smtp_user,self.useremail)
				server.sendmail(smtp_user,self.useremail,msg.as_string())
		except Exception as e:
			print(e)

	# Function to onboard ticket	
	def registerComplaint(self)->bool:
		return True


imap_host = 'mail.nullbyte.exe'
imap_user = ADMIN_CRED['username'] or ADMIN_CRED_2['username'] 
imap_pass = ADMIN_CRED['password'] or ADMIN_CRED_2['password']
print(imap_host,imap_user,imap_pass)
imap = imaplib.IMAP4_SSL(imap_host)
imap.login(imap_user, imap_pass)
imap.select('Inbox')
tmp, data = imap.search(None, 'ALL')
print(len(data))
for num in reversed(data[0].split()):
	tmp, data = imap.fetch(num, '(RFC822)')
	msgdata=data[0][1]
	moj=mailobj()
	moj.parsemail(msgdata)
	break
imap.close()