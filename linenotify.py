#!usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.parse
import pycurl,time 

#--https://notify-bot.line.me/my/ 
#--you must generate token_key here first.
#token_key = '<your token_key>'
headers = str("Authorization: Bearer "+token_key)

#--LINE Notify Image File
def line_notifyIMG(xmessage,imagefile,xheaders):
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, 'https://notify-api.line.me/api/notify')
	curl.setopt(pycurl.HTTPHEADER, [headers])

	curl.setopt(pycurl.HTTPPOST, [
	('message', xmessage.encode('utf-8')),
	('imageFile', (curl.FORM_FILE, str(imagefile))) ])

	curl.perform()

	xtxt = ('Status=%d total time=%5.3f' % (curl.getinfo(curl.RESPONSE_CODE), curl.getinfo(curl.TOTAL_TIME)))
	return xtxt

#--LINE Notify sticker
def line_notifySTK(xmessage,stkpid,stkid,xheaders):
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, 'https://notify-api.line.me/api/notify')
	curl.setopt(pycurl.HTTPHEADER, [xheaders])

	curl.setopt(pycurl.HTTPPOST, [
	('message', xmessage.encode('utf-8')),
	('stickerPackageId', str(stkpid)),
	('stickerId', str(stkid)) ])

	curl.perform()

#--LINE Notify Message
def line_notifyMSG(xmessage,xheaders):
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL,'https://notify-api.line.me/api/notify')
	curl.setopt(pycurl.HTTPHEADER,[xheaders])
	curl.setopt(pycurl.HTTPPOST,[('message', xmessage.encode('utf-8'))])
	curl.perform()

if __name__ == "__main__":
	'''
	xmsg=("ทดสอบส่งสติกเกอร์  วัน-เวลา %s" % (time.ctime()))
	stkpid = 1
	stkid = 115
	line_notifySTK(xmsg,stkpid,stkid,headers)

	xmsg=("ทดสอบส่งข้อความภาษาไทย  วัน-เวลา %s" % (time.ctime()))
	line_notifyMSG(xmsg,headers)
	'''

	xfile ='myphoto2.png'
	xmsg=("%s รูปภาพดญ.โปรแกรม  วัน-เวลา %s" % (xfile,time.ctime()))
	xtxt = line_notifyIMG(xmsg,xfile,headers)
	print (xtxt)

