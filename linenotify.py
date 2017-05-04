#!usr/bin/python3
# -*- coding: utf-8 -*-


#with---timeout error curl.perform()...


import urllib.parse
import pycurl,time 

#--https://notify-bot.line.me/my/ 
#--you must generate token_key here first.
token_key = '<your token_key>'
headers = str("Authorization: Bearer "+token_key)
mytimeout = 5

#--LINE Notify Image File
def line_notifyIMG(xmessage,imagefile,xheaders):
	curl = pycurl.Curl()
	curl.setopt(pycurl.CONNECTTIMEOUT,mytimeout)

	curl.setopt(pycurl.URL, 'https://notify-api.line.me/api/notify')
	curl.setopt(pycurl.HTTPHEADER, [headers])
	curl.setopt(pycurl.HTTPPOST, [
	('message', xmessage.encode('utf-8')),
	('imageFile', (curl.FORM_FILE, str(imagefile))) ])

	try:
		print (">> Try posting message+upload image: \n message = '%s' \n imagefile = %s" % (xmessage,imagefile))
		curl.perform()
	except:
		pass

	xrtn = (curl.getinfo(curl.RESPONSE_CODE), curl.errstr(), curl.getinfo(curl.TOTAL_TIME))
	curl.close()
	return xrtn

#--LINE Notify sticker
def line_notifySTK(xmessage,stkpid,stkid,xheaders):
	curl = pycurl.Curl()
	curl.setopt(pycurl.CONNECTTIMEOUT,mytimeout)
	curl.setopt(pycurl.URL, 'https://notify-api.line.me/api/notify')
	curl.setopt(pycurl.HTTPHEADER, [xheaders])

	curl.setopt(pycurl.HTTPPOST, [
	('message', xmessage.encode('utf-8')),
	('stickerPackageId', str(stkpid)),
	('stickerId', str(stkid)) ])

	try:
		print (">> Try posting message+stickerPID/ID: \n message ='%s' \n stickerPID/ID =  %i/%i" % (xmessage,stkpid,stkid))
		curl.perform()
	except:
		pass

	xrtn = (curl.getinfo(curl.RESPONSE_CODE), curl.errstr(), curl.getinfo(curl.TOTAL_TIME))
	curl.close()
	return xrtn

#--LINE Notify Message
def line_notifyMSG(xmessage,xheaders):
	curl = pycurl.Curl()
	curl.setopt(pycurl.CONNECTTIMEOUT,mytimeout)
	curl.setopt(pycurl.URL,'https://notify-api.line.me/api/notify')
	curl.setopt(pycurl.HTTPHEADER,[xheaders])
	curl.setopt(pycurl.HTTPPOST,[('message', xmessage.encode('utf-8'))])

	try:
		print (">> Try posting message: \n message = '%s'" % xmessage)
		curl.perform()
	except:
		pass

	xrtn = (curl.getinfo(curl.RESPONSE_CODE), curl.errstr(), curl.getinfo(curl.TOTAL_TIME))
	curl.close()
	return xrtn

if __name__ == "__main__":
	
	xmsg=("ทดสอบส่งข้อความภาษาไทย  วัน-เวลา %s" % (time.ctime()))
	xrtn = line_notifyMSG(xmsg,headers)
	print ('>> status , errorstring , total time \n   ',xrtn,'\n')
	
	
	xmsg=("ทดสอบส่งสติกเกอร์  วัน-เวลา %s" % (time.ctime()))
	stkpid = 1
	stkid = 115
	xrtn = line_notifySTK(xmsg,stkpid,stkid,headers)
	print ('>> status , errorstring , total time \n   ',xrtn,'\n')
	

	
	xfile ='myphoto2.png'
	xmsg=("%s รูปภาพดญ.โปรแกรม  วัน-เวลา %s" % (xfile,time.ctime()))
	xrtn = line_notifyIMG(xmsg,xfile,headers)
	print ('>> status , errorstring , total time \n   ',xrtn,'\n')


