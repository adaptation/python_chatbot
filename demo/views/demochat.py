# -*- coding: utf-8 -*-
# Commonモジュール
import json
import io
import os
from decimal import *
from django.shortcuts import render
from django.contrib import messages
from django.http.response import JsonResponse
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *

import subprocess

from datetime import datetime

# メール送信モジュールのimport
from . import sendmail_module

# Log関連
import logging
logger = logging.getLogger('simplelogger')

# gazetteer。未組み込み。
physicalConditionGazetteer = ["具合","体調","熱","風邪","頭","お腹","咳"]
someWorkGazetteer = ["","","",""]

# 休暇届ファイル名。メール送信モジュール呼び出し用
OUTPUT_FILE_NAME = "休暇届.xlsx"

# 未実装の入力値を定義
TENTATIVE_USER_NAME = "アンディ"
TENTATIVE_USER_MAILADDRESS = "CC送信先メールアドレス@XXX 要するにアンディのメールアドレス"
TENTATIVE_DATE_RANGE = 1

# 会話の状態を示す定数
STATUS_INIT = "init"
STATUS_STANDBY = "standby"
STATUS_COMPLETE = "complete"
"""
状態：会話の状態
	init：初期状態
	standby:情報待ち
	complete:全情報取得完了
	
	※発話サイクル
	メッセージ表示	→	メッセージ入力
		↑					↓
	メッセージ生成		言語解析
		↑					↓
	行動選択		←	状態更新
	
	必要な要素：
	Intention：意思
	Reason：理由
	Datetime：日数
	
"""

# 初回表示
def index(request):
	logger.debug("初回リクエスト")
	msgMng = ChatMessage() # メッセージ管理インスタンス
	chatsession = ChatSession() # セッション管理インスタンス
	
	# セッションID発行
	# sessionid = chatsession.getSession()
	
	# 初回システムメッセージ生成
	msg = msgMng.createGreeting()
	
	# サーバーデータをテンプレートへ受け渡し
	context ={}
	context["firstmsg"] = msg
	# context["sessionid"] = sessionid
	# context["sessionmng"] = chatsession
	request.session["status"] = chatsession.getStatus()
	
	# チャット画面描画
	return render(request, 'dev/demochat.html', context)

# 会話応答
def conversation(request):
	"""
	demochat画面からjsonで発信されたメッセージを受け取るメソッド。
	"""

	try:
		msgMng = ChatMessage() # メッセージ管理インスタンス

		# メッセージ取得
		user_msg = request.POST["utterance"]

		# セッションから会話の状態を取得
		status = request.session["status"]

		if status == STATUS_INIT:
			# 初期状態
			# 発話解析
			words = msgMng.extractWords(user_msg)
			if len(words) <= 1: # 主語、述語がなければ定型文を返却
				res = json.dumps({'resmsg':'よくわかんないな。。'})
				return HttpResponse(res)

			msgMng.analyzeMessage(words)

			# セッションに会話の状態と休暇の理由を保持。
			# 休暇の理由は厳密に言葉を変換する必要があるが、暫定。
			request.session["status"] = STATUS_STANDBY
			request.session["reason"] = msgMng.getSystemMessage()

			resmsg = 'おーけー！！<br>' + msgMng.getSystemMessage() + 'んだな。<br>休むかい？'
			resmsg = resmsg + "<input type=\"button\" value=\"はい\" class='form-control makekyukabtn'>"
			res = json.dumps({'resmsg':resmsg})

		elif status == STATUS_STANDBY:
			# 情報待ち
			"""
			TODO:応答メッセージ解析埋め込み
			"""

			username = TENTATIVE_USER_NAME
			reason = request.session["reason"]

			# 休暇届メールの送信
			ret = sendmail_module.main(OUTPUT_FILE_NAME, username, reason, TENTATIVE_USER_MAILADDRESS)
			if ret == 0:
				# 送信成功
				res = json.dumps({'resmsg':'おーけー！！<br>会社には僕からメールを送っておいたぜ！'})
				request.session["status"] = STATUS_COMPLETE
			else:
				# 送信失敗
				res = json.dumps({'resmsg':'あれれ……。<br>今は会社にメールを送れないみたい。<br>悪いけど、直接連絡してくれないかな…。'})
				request.session["status"] = STATUS_INIT

		elif status == STATUS_COMPLETE:
			# 全情報取得完了の状態からは定型文を返す
			res = json.dumps({'resmsg':'早く休めよ！'})
			request.session["status"] = STATUS_INIT


		return HttpResponse(res)
	except Exception as e:
		logger.exception(e)

	
# 休暇届け作成
def makeExcel(request):
	batchPath = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/").replace("demo/views", "tools/excel_action.bat")
	subprocess.run(batchPath + " 樗木辰哉 体調不良 1")

	res = json.dumps({'resmsg':'おーけー！！<br>' +
		'休暇届を作成したぜ。'})
	return HttpResponse(res)

"""
セッション管理クラス

"""
class ChatSession():
	def __init__(self):
		self.sessionId = "abcdefg"
		self.status = STATUS_INIT
	
	# セッション取得
	def getSession(self):
		return self.sessionId
		
	# 状態取得
	def getStatus(self):
		return self.status

"""
メッセージ管理クラス

"""
class ChatMessage():
	def __init__(self):
		pass
	
	# 初回メッセージ生成
	def createGreeting(self):
		firstMsg = ""
		secondMsg = ""
		
		# 現在のサーバー時刻により、あいさつを設定する
		now = int(datetime.now().strftime("%H"))
		if now >= 4 and now < 12:	# 4時以降～12時以前は午前中
			firstMsg =  "おはよう、"
		elif now >= 12 and now < 17: # 12時以降～17時以前は午後
			firstMsg =  "こんにちは、"
		else:						# 上記時間帯以外は夜
			firstMsg =  "こんばんは、"
		firstMsg = firstMsg + TENTATIVE_USER_NAME + "\n"
		secondMsg = "今回の用件はなんだい？？"
		
		return firstMsg + secondMsg
	
	# わかち書き
	def extractWords(self, text):
		t = Tokenizer()
		tokens = t.tokenize(text)
		#for tmp in tokens:
		#	print(tmp)
		
		print('\r\n')
		ana = Analyzer(token_filters=[CompoundNounFilter()])
		for token in ana.analyze(text):
			print(token)
		
		return [token.base_form for token in tokens
			#if token.part_of_speech.split(',')[0] in['名詞', '助詞', '動詞']]
			if token.part_of_speech.split(',')[0] in['名詞', '動詞', '形容詞']]
			
	# 解析
	def analyzeMessage(self, msgs):
		self.syugo = msgs[0]
		self.jyutsugo = msgs[len(msgs)-1]
		
		# 原因に対する応答を構築
		self.makeMessage(1)
	
	# 応答メッセージ生成
	def makeMessage(self, action):
		if action == 1: # 原因応答
			self.systemmsg = self.syugo + "が" + self.jyutsugo
	
	def getSystemMessage(self):
		return self.systemmsg
