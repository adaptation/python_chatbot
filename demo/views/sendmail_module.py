"""
メール送信モジュール
"""
import os
import datetime
import smtplib
import mimetypes
import logging

from argparse import ArgumentParser
from email.message import EmailMessage
from email.policy import SMTP

FROM_ADDR_NAME = u"休暇届自動送信システム"
FROM_ADDRESS = "送信元メールアドレス@gmail.com"
TO_ADDRESS = "送信先メールアドレス@gmail.com"
ATTACHED_FILE_PATH = r"添付ファイル格納先ディレクトリ/tools/output/"

# メールを送信するSMTPサーバを指定
"""
テスト用としてGmailのSMTPサーバを指定しています。
Googleアカウントの設定から「安全性の低いアプリのアクセス」を「有効」にする必要があります。
https://support.google.com/mail/answer/7126229?hl=ja&visit_id=636859852643918914-82946651
"""
SMTP_SERVER_HOST = "smtp.gmail.com"
SMTP_SERVER_PORT = 587
SMTP_LOGIN_ID = "Googleアカウント XXX@gmail.com"
SMTP_LOGIN_PASSWORD = "Googleログインパスワード"

def main(attached_file_name, applicant, reason, applicant_address):
	"""
	休暇届メールを送信します。
	届け出者のメールアドレスにCC送信します。
	
	引  数  1:添付Excelファイル名 
	        2:届け出者名
	        3:届け出理由
	        4:届け出者メールアドレス
	
	戻り値  0:正常終了
	        1:異常終了
	"""
	
	def create_body(applicant):
		"""
		本文生成関数
		"""
		body = "このメッセージは休暇届自動送信システムから送信されています。\r\n"\
		       "\r\n"\
		       "届け出者：" + applicant + "\r\n"\
		       "理由：" + reason + "\r\n"\
		       "\r\n"
		return body
	
	def create_message(from_addr, to_addr, cc_addr, subject, body, mime, attach_file):
		"""
		メール生成関数
		"""
		msg = EmailMessage()
		msg["Subject"] = subject
		msg["From"] = FROM_ADDR_NAME + "<" + from_addr + ">"
		msg["To"] = to_addr
		msg["Cc"] = cc_addr
		msg["Date"] = datetime.datetime.now()
		msg.set_content(body)
		
		# 添付ファイルの組み込み
		file = open(attach_file['path'], 'rb')
		msg.add_attachment(file.read(), maintype=mime['type'], subtype=mime['subtype'], filename=attach_file['name'])
		file.close()
		
		return msg
	
	def send(from_addr, to_addr, msg):
		"""
		メールを送信関数
		"""
		smtp = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
		smtp.login(SMTP_LOGIN_ID, SMTP_LOGIN_PASSWORD)
		smtp.sendmail(from_addr, to_addr, msg.as_string())
		smtp.quit()
	
	# 実行するのはここから
	from_addr = FROM_ADDRESS
	to_addr = TO_ADDRESS
	cc_addr = applicant_address
	subject = "休暇届自動送信システム(" + applicant + ")"
	body = create_body(applicant)
	mime={'type':'application', 'subtype':'excel'}
	attach_file={'name':attached_file_name, 'path':ATTACHED_FILE_PATH + attached_file_name}
	
	try:
		msg = create_message(from_addr, to_addr, cc_addr, subject, body, mime, attach_file)
		# raise
		send(from_addr, to_addr, msg)
		return 0
		
	except Exception as e:
		logging.exception(e)
		return 1

