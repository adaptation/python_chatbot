# -*- coding: utf-8 -*-
from django.conf.urls import include,url
from .views import demochat

urlpatterns = [
	url(r'^demochat/$', demochat.index, name='index')
	,url(r'^demochat/conversation$', demochat.conversation, name='conversation')
	,url(r'^demochat/makekyuka$', demochat.makeExcel, name='makeExcel') # ‹x‰É“Í‚¯ì¬
]

