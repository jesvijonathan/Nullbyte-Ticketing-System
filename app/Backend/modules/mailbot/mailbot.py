import imaplib
import re
import email
import smtplib
from email.mime.text import MIMEText
from config import *
import time
import hashlib
import modules.ml.ml_handler as ml_handler
import base64

class MailObj:
	def __init__(self):
		self.username = ""
		self.useremail = ""
		self.subject = ""
		self.body = ""
		self.attachment = []
		self.message_id = ""
		self.in_reply_to = ""
		self.references = ""

	def parse_mail(self, mail_obj):
		try:
			msg = email.message_from_bytes(mail_obj)
			from_user = msg['From']
			subject = msg['Subject'] if msg['Subject'] else ""
			body = ""
			self.message_id = msg['Message-ID']
			self.in_reply_to = msg['In-Reply-To']
			self.references = msg['References']
			
			for part in msg.walk():
				if part.get_content_type() == 'text/plain' and part.get_content_disposition() is None:
					body = part.get_payload(decode=True).decode(part.get_content_charset())
				elif part.get_content_disposition() == 'attachment':
					file_data = base64.b64encode(part.get_payload(decode=True))
					filename = part.get_filename()
					size_mb = len(file_data) / (1024 * 1024)
					self.attachment.append({
						'file_name': filename,
						'file_data': file_data,
						'size_mb': f"{size_mb:.2f}"
					})
			
			self.useremail = re.search(r'<([^>]+)>', from_user).group(1)
			self.username = re.search(r'^([^<]+)', from_user).group(1).strip()
			self.body = body
			self.subject = subject
			if self.register_complaint():
				self.create_reply()
		except Exception as e:
			print(f"Failed to parse mail: {e}")

	def create_reply(self):
		smtp_host = 'mail.nullbyte.exe'
		smtp_user = MAIL_CRED['username']
		smtp_pass = MAIL_CRED['password']
		try:
			tempsub = self.subject[4:] if self.subject.startswith("Re: ") else self.subject
			mailchainhash = hashlib.sha256(f"{str(self.useremail)}{str(tempsub)}".encode()).hexdigest()
			payload = {"upn": self.useremail}

			mailchains[mailchainhash] = ml_handler.ChatbotHandler(mailchainhash, None, payload=payload,medium=2)

			handler=mailchains[mailchainhash]
			print(f"Mail chain hash: {mailchainhash}")

			# remove empty lines from mail and signature lines
			self.body = re.sub(r'\n+', '\n', self.body)
			self.body = re.sub(r'--\n.*', '', self.body)
			self.body = re.sub(r'On .*, .* wrote:\n', '', self.body)
			if mailchains[mailchainhash]:
				query=f"Subject: {self.subject}\n{self.body}"
			else:
				query=self.body
			handler.response_add(query, self.attachment)
			print("Mail Response:")
			
			print(handler.mail["response"])
			print("Mailchainhash:",mailchainhash)

			while handler.mail["processing"]:
				time.sleep(1)
			body = handler.mail["response"]
			mailbot=handler.mail["RepliedBot"]
			body += f'\n\nBest Regards,\n{mailbot}'

			msg = MIMEText(body)
			msg['Subject'] = self.subject
			msg['From'] = smtp_user
			msg['To'] = self.useremail
			msg['In-Reply-To'] = self.message_id
			msg['References'] = self.references if self.references else self.message_id

			with smtplib.SMTP_SSL(smtp_host, 465) as server:
				server.login(smtp_user, smtp_pass)
				server.sendmail(smtp_user, self.useremail, msg.as_string())
			print(f"Reply sent to {self.username} ({self.useremail})")
		except smtplib.SMTPException as e:
			print(f"SMTP error: {e}")
		except Exception as e:
			print(f"Failed to create reply: {e}")

	def register_complaint(self) -> bool:
		return True

class MailBot:
	def __init__(self):
		self.imap_host = 'mail.nullbyte.exe'
		self.imap_user = MAIL_CRED['username']
		self.imap_pass = MAIL_CRED['password']

	def poll_inbox(self):
		while True:
			try:
				imap = imaplib.IMAP4_SSL(self.imap_host)
				imap.login(self.imap_user, self.imap_pass)
				if imap.select('Inbox')[0] != 'OK':
					print("Error in selecting Inbox")
					imap.logout()
					time.sleep(2)
					continue
				tmp, data = imap.search(None, 'UNSEEN')
				for num in reversed(data[0].split()):
					tmp, data = imap.fetch(num, '(RFC822)')
					msg_data = data[0][1]
					moj = MailObj()
					moj.parse_mail(msg_data)
				imap.close()
				imap.logout()
			except imaplib.IMAP4.error as e:
				print(f"IMAP error: {e}")
			except Exception as e:
				print(f"Error polling inbox: {e}")
			time.sleep(2)
