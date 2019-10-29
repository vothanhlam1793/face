#!/usr/bin/python
# -*- coding: utf8 -*-
########################################################################
#API face detect setup
########################################################################
import json
import requests
import base64
from datetime import datetime
from ftplib import FTP
import time
import os

import threading
from MqttClient import MQTTClient

Mqtt = MQTTClient()
Mqtt.MqttPathPublish = "your path to publish"
Mqtt.MqttPathSubcribe = "APIGetPost"

def getDataMqtt():
    __waitData = Mqtt.getData()
    if (__waitData != None): 
        try:
            _waitData = json.loads(__waitData)
            return _waitData
        except ValueError as e:
            print "error: ", str(e)
            return False
    else:
        return False

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        Mqtt.mqttSubcribe()

#queueLock = threading.Lock()
thread = myThread(1, "thread1")
thread.start()

#############################################################
class RegiterThread (threading.Thread):
    def __init__(self, ___dataWriteMainAppthread,___userName,___ID,___VideoBase64,___ImageBase64,___isPortrait,___overWrite):
        threading.Thread.__init__(self)
        self.___dataWriteMainAppthread = ___dataWriteMainAppthread
        self.___userName = ___userName
        self.___ID = ___ID
        self.___VideoBase64 = ___VideoBase64
        self.___ImageBase64 = ___ImageBase64
        self.___isPortrait = ___isPortrait
        self.___overWrite = ___overWrite
    def run(self):
        RegiterUserThread(self.___dataWriteMainAppthread,self.___userName,self.___ID,self.___VideoBase64,self.___ImageBase64,self.___isPortrait,self.___overWrite)
def RegiterUserThread(_dataWriteMainAppthread, __userName, __ID, __VideoBase64, __ImageBase64, __isPortrait, __overWrite):
    __timeStart = time.time()
    _dataWriteMainAppthread["data"]["ID"] = __ID
    if not os.path.isfile(__VideoBase64):
        print "Image register path: " + __VideoBase64 + " from Mqtt is not exist"
        _dataWriteMainAppthread["data"]["mess"] = "video path is not exist!"
        Mqtt.MqttPathPublish = "MainApp"
        Mqtt.mqttPublish(json.dumps(_dataWriteMainAppthread))
        print _dataWriteMainAppthread
        return False
    # __timeName = datetime.now()
    # _timeName = str(__timeName.strftime("%M:%S"))
    # if os.path.isfile("/home/pi/maychamcong/video/video"+_timeName+".mp4"):
    #     os.system("rm /home/pi/maychamcong/video/video"+_timeName+".mp4")
    # os.system("ffmpeg -i " + __VideoBase64 + " " + "/home/pi/maychamcong/video/video"+_timeName+".mp4")
    # # __videoFile = open(__VideoBase64,"rb")
    # __videoFile = open("/home/pi/maychamcong/video/video"+_timeName+".mp4","rb")
    # ___VideoBase64_sent = base64.b64encode(__videoFile.read())
    # __videoFile.close()
    FTPVideo_ = saveVideoFtp(ftpHost,ftpUser,ftpPass,ftpPath,__VideoBase64)
    if FTPVideo_ == False:
        _dataWriteMainAppthread["data"]["mess"] = "image path is not exist!"
        Mqtt.MqttPathPublish = "MainApp"
        Mqtt.mqttPublish(json.dumps(_dataWriteMainAppthread))
        print _dataWriteMainAppthread
        return False
    # #print VideoBase64
    # __timeStart = time.time()
    print "start"
    _respontRegiter = registerUserFTP(ftpHost,ftpUser,ftpPass,__userName,__ID,FTPVideo_,__isPortrait,__overWrite)
    # _respontRegiter = registerUser(__userName,__ID,___VideoBase64_sent,__isPortrait,__overWrite)
    print "stop"
    # __timeStop = time.time()
    # if os.path.isfile('/home/pi/maychamcong/log.txt'):
    #     _data = open('/home/pi/maychamcong/log.txt', 'a')
    #     print __timeStop-__timeStart
    #     now = datetime.now()
    #     _data.write("regiterUser " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
    #     _data.write(str('total run-time of API in second: %fs\n\n' % (__timeStop-__timeStart)))
    #     _data.close()
    # else:
    #     print "file log.txt is not exist"
    #print _respont
    if _respontRegiter["message"] == "SUCCESS":
        #_dataWriteMainAppthread["data"]["ID"] = _respontRegiter["data"]["user_id"]
        # print "start verify for register!"
        # __timeStart = time.time()
        # __respontthread = verifyFaceFtp(ftpHost,ftpUser,ftpPass,FtpImage,__ID)
        # __timeStop = time.time()
        # if os.path.isfile('/home/pi/maychamcong/log.txt'):
        #     _data = open('/home/pi/maychamcong/log.txt', 'a')
        #     print __timeStop-__timeStart
        #     _now = datetime.now()
        #     _data.write("verify " + str(_now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
        #     _data.write(str('total run-time of API in second: %fs\n\n' % (__timeStop-__timeStart)))
        #     _data.close()
        # else:
        #     print "file log.txt is not exist"
        # if __respontthread["message"] == "SUCCESS":
        #     #print __respont
        #     if __respontthread["data"]["result"][0]["message"] == "Matched":
        #         _dataWriteMainAppthread["data"]["mess"] = "user is added but no training"
        print "start train"
        _a_timeStart = time.time()
        # __respontRetraint = reTrainClound()
        __respontRetraint = reTrainClound()
        _a_timeStop = time.time()
        if os.path.isfile('/home/pi/maychamcong/log.txt'):
            _data = open('/home/pi/maychamcong/log.txt', 'a')
            print _a_timeStop-_a_timeStart
            _now = datetime.now()
            _data.write("retrain cloud API" + str(_now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
            _data.write(str('total run-time of API in second: %fs\n\n' % (_a_timeStop-_a_timeStart)))
            _data.close()
        else:
            print "file log.txt is not exist"
        if __respontRetraint["message"] == "SUCCESS":
            print "retrain clound successfull"
            _dataWriteMainAppthread["data"]["status"] = True
	    _dataWriteMainAppthread["data"]["mess"] = "user is added and ready to use"
            __timeStop = time.time()
            if os.path.isfile('/home/pi/maychamcong/log.txt'):
                _data = open('/home/pi/maychamcong/log.txt', 'a')
                print __timeStop-__timeStart
                now = datetime.now()
                _data.write("regiterUser and retrain " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
                _data.write(str('total run-time of API in second: %fs\n\n' % (__timeStop-__timeStart)))
                _data.close()
            else:
                print "file log.txt is not exist"
        else:
            print __respontRetraint
            print "can't retrain user!"
            _dataWriteMainAppthread["data"]["mess"] = "user is added but no training"        #     else:
        #         print "image and video is not 1 people!"
        #         _dataWriteMainAppthread["data"]["mess"] = "user is not math with video"
        # else:
        #     print __respontthread
        #     print "can't verify image!"
        #     _dataWriteMainAppthread["data"]["mess"] = "can not verify image with user"
    else:
        print _respontRegiter
        print "can't register user!"
        _dataWriteMainAppthread["data"]["mess"] = "can not register,maybe video too large"

    print _dataWriteMainAppthread
    Mqtt.MqttPathPublish = "MainApp"
    Mqtt.mqttPublish(json.dumps(_dataWriteMainAppthread))
    return True
#############################################################

#login infomation
# urlLogin = "http://new-thd.ddns.net:4000/v1/auth"
urlLogin = "https://api.deepkafe.com/faceid/v1/auth"
typeHeaderLogin = {'Content-Type': 'application/json'}
userData = {"username": "creta",  "password": "creta"}

#API Upload
# urlDac = "http://new-thd.ddns.net:4000/v1/dac"
urlDac = "https://api.deepkafe.com/faceid/v1/dac"

#Get access data
# urlGetAccess = "http://new-thd.ddns.net:4000/v1/fetch"
urlGetAccess = "https://api.deepkafe.com/faceid/v1/fetch"
dataGetAccess = {"start_time": "01/01/1992 1:1:1", "end_time": "06/03/2019 1:1:1"}

#Verification API
# urlVerify = "http://new-thd.ddns.net:4000/v1/verify"
urlVerify = "https://api.deepkafe.com/faceid/v1/verify"
dataVerify = {'image': '',  'verify_id' : ''}
urlVerifyFtp = "https://api.deepkafe.com/faceid/v1/ftp-verify-notice"
dataVerifyFtp = {"ftp_host": "", "ftp_user": "", "ftp_pass": "", "verify_data": [1]}

#Get all user API
# urlGetUsers = "http://new-thd.ddns.net:4000/v1/get_users"
urlGetUsers = "https://api.deepkafe.com/faceid/v1//get_all_member"
dataGetUsers = {"max_person_images": 5}

#Register User API
# urlRegister = "http://new-thd.ddns.net:4000/v1/register"
urlRegister = "https://api.deepkafe.com/faceid/v1/register"
dataRegister = {"user_name": "",  "user_id" : "",  "face_images" : [], "videos": [1], "isPortrait": False , "overwrite": True}

#Register User API with FTP
# urlRegister = "http://new-thd.ddns.net:4000/v1/register"
urlRegisterFTP = "https://api.deepkafe.com/faceid/v1/ftp-register"
dataRegisterFTP = {"ftp_host": "", "ftp_user": "", "ftp_pass": "", "user_name": "",  "user_id" : "",  "face_images" : [], "videos": [1], "isPortrait": False , "overwrite": True}

#Retrain API
# urlRetrain = "http://new-thd.ddns.net:4000/v1/retrain"
urlRetrain = "https://api.deepkafe.com/faceid/v1/retrain"

#Retrain clound API
# urlRetrainClound = "http://new-thd.ddns.net:4000/v1/cloud-recognize-retrain"
urlRetrainClound = "https://api.deepkafe.com/faceid/v1/cloud-recognize-retrain"

#Delete User API
# urlDeleteUser = "http://new-thd.ddns.net:4000/v1/delete_user"
urlDeleteUser = "https://api.deepkafe.com/faceid/v1/delete_user"
dataDeleteUser = {"user_id" : ""}

#Recognize by FTP API
urlRecognize = "https://api.deepkafe.com/faceid/v1/ftp-recognize-notice"
dataRecognize = {"ftp_host": "", "ftp_user": "", "ftp_pass": "", "recognize_data": [""]}

typeHeaderApi = {'Content-Type': 'application/json', 'Authorization':''}


def getToken():
    responseDecodedJson = requests.post(urlLogin, data=json.dumps(userData), headers=typeHeaderLogin)
    #print responseDecodedJson
    try:
        responseJson = responseDecodedJson.json()
        if responseJson["message"] == "SUCCESS":
            return responseJson["data"]["authToken"].encode("ascii","replace")
        else:
            print "Get token error!"
            return False
    except ValueError as e:
        print "Error: ", str(e)
        return False

def getAccess(_startTime, _endTime):
    dataGetAccess["start_time"] = _startTime
    dataGetAccess["end_time"] = _endTime
    _token = getToken()
    if not _token:
        return "False"
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    responseDecodedJson = requests.post(urlGetAccess, data=json.dumps(dataGetAccess), headers=typeHeaderApi)
    try:
        responseJson = responseDecodedJson.json()
        return responseJson
    except ValueError as e:
        print "Error: ", str(e)
        return False

def verifyFace(_base64Image, _id):
    dataVerify['image'] = _base64Image
    dataVerify['verify_id'] = _id
    _token = getToken()
    if not _token:
        return False
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    responseDecodedJson = requests.post(urlVerify, data=json.dumps(dataVerify), headers=typeHeaderApi)
    try:
        responseJson = responseDecodedJson.json()
        return responseJson
    except ValueError as e:
        print "Error: ", str(e)
        return False

def verifyFaceFtp(_ftpHost, _ftpUser, _ftpPass, _imageFtp, _ID):
    dataVerifyFtp['ftp_host'] = _ftpHost
    dataVerifyFtp['ftp_user'] = _ftpUser
    dataVerifyFtp['ftp_pass'] =_ftpPass
    dataVerifyFtp['verify_data'][0] = [_imageFtp,_ID]
    _token = getToken()
    if not _token:
        return False
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    responseDecodedJson = requests.post(urlVerifyFtp, data=json.dumps(dataVerifyFtp), headers=typeHeaderApi)
    try:
        responseJson = responseDecodedJson.json()
        return responseJson
    except ValueError as e:
        print "Error: ", str(e)
        return False

def getAllUsers(_number):
    _token = getToken()
    if not _token:
        return False
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    dataGetUsers["max_person_images"] = _number
    responseDecodedJson = requests.post(urlGetUsers, data=json.dumps(dataGetUsers), headers=typeHeaderApi)
    try:
        responseJson = responseDecodedJson.json()
        return responseJson
    except ValueError as e:
        print "Error: ", str(e)
        return False

def registerUser(_username, _userId, _videosbase64, _isPortrait, _overwrite):
    _token = getToken()
    if not _token:
        return False
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    dataRegister["user_name"] = _username
    dataRegister["user_id"] = _userId
    #dataRegister["face_images"][0] = _faceImage
    dataRegister["videos"][0] = _videosbase64
    dataRegister["isPortrait"] = _isPortrait
    dataRegister["overwrite"] = _overwrite
    #print dataRegister
    responseDecodedJson = requests.post(urlRegister, data=json.dumps(dataRegister), headers=typeHeaderApi)
    #print responseDecodedJson
    # tt = open("request.txt","wb")
    # tt.write(json.dumps(dataRegister))
    # tt.close()
    #print len(json.dumps(dataRegister))
    try:
        responseJson = responseDecodedJson.json()
        return responseJson
    except ValueError as e:
        print "Error: ", str(e)
        return False

def registerUserFTP(_ftpHost, _ftpUser, _ftpPass,_username, _userId, _videosbase64, _isPortrait, _overwrite):
    _token = getToken()
    if not _token:
        return False
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    dataRegisterFTP['ftp_host'] = _ftpHost
    dataRegisterFTP['ftp_user'] = _ftpUser
    dataRegisterFTP['ftp_pass'] =_ftpPass
    dataRegisterFTP["user_name"] = _username
    dataRegisterFTP["user_id"] = _userId
    #dataRegisterFTP["face_images"][0] = _faceImage
    dataRegisterFTP["videos"][0] = _videosbase64
    dataRegisterFTP["isPortrait"] = _isPortrait
    dataRegisterFTP["overwrite"] = _overwrite
    responseDecodedJson = requests.post(urlRegisterFTP, data=json.dumps(dataRegisterFTP), headers=typeHeaderApi)
    #print len(json.dumps(dataRegisterFTP))
    try:
        responseJson = responseDecodedJson.json()
        return responseJson
    except ValueError as e:
        print "Error: ", str(e)
        return False


def deleteUser(_userId):
    _token = getToken()
    if not _token:
        return False
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    dataDeleteUser["user_id"] = _userId
    responseDecodedJson = requests.post(urlDeleteUser, data=json.dumps(dataDeleteUser), headers=typeHeaderApi)
    try:
        responseJson = responseDecodedJson.json()
        return responseJson
    except ValueError as e:
        print "Error: ", str(e)
        return False

def recognizeFaceFtp(_ftpHost, _ftpUser, _ftpPass, _imageFtp):
    dataRecognize["ftp_host"] = _ftpHost
    dataRecognize["ftp_user"] = _ftpUser
    dataRecognize["ftp_pass"] =_ftpPass
    dataRecognize["recognize_data"][0] = _imageFtp
    _token = getToken()
    if _token == "False":
        return "False"
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    #print dataRecognize
    responseDecodedJson = requests.post(urlRecognize, data=json.dumps(dataRecognize), headers=typeHeaderApi)
    try:
        responseJson = responseDecodedJson.json()
        return responseJson
    except ValueError as e:
        print "Error: ", str(e)
        return False

def reTrain():
    _token = getToken()
    if _token == "False":
        return "False"
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    responseDecodedJson = requests.get(urlRetrain, headers=typeHeaderApi)
    try:
        responseJson = responseDecodedJson.json()
        return responseJson
    except ValueError as e:
        print "Error: ", str(e)
        return False

def reTrainClound():
    _token = getToken()
    if _token == "False":
        return "False"
    typeHeaderApi['Authorization'] = 'Bearer ' + _token
    responseDecodedJson = requests.get(urlRetrainClound, headers=typeHeaderApi)
    try:
        responseJson = responseDecodedJson.json()
        return responseJson
    except ValueError as e:
        print "Error: ", str(e)
        return False

########################################################################
def saveImageFtp(_host,_user,_pass,_path,_image):
    try: 
        FtpImage = "Image_" + datetime.now().strftime("%b-%d-%Y_%H_%M_%S")+".jpg"
        if not os.path.isfile(_image):
            print "Image path from Mqtt is not exist"
            return False
        fp = open(_image, 'rb')
        ftp.connect(_host)
        ftp.login(_user,_pass)
        ftp.cwd(_path)
        ftp.storbinary('STOR %s' % FtpImage, fp)
        fp.close()
        ftp.quit()
        return (_path + "/" + FtpImage)
    except Exception as e:
        print "error: ", e
        return False

def saveVideoFtp(_host,_user,_pass,_path,_video):
    try: 
        _FTPVideo = "Video_" + datetime.now().strftime("%b-%d-%Y_%H_%M_%S")+".webm"
        if not os.path.isfile(_video):
            print "Image path from Mqtt is not exist"
            return False
        fp = open(_video, 'rb')
        ftp.connect(_host)
        ftp.login(_user,_pass)
        ftp.cwd(_path)
        ftp.storbinary('STOR %s' % _FTPVideo, fp)
        fp.close()
        ftp.quit()
        return (_path + "/" + _FTPVideo)
    except Exception as e:
        print "error: ", e
        return False

flag_1 = False
flag_2 = False
_dataWriteMainApp = {"source":"APIGetPost","func":"screen","data":[]}
_dataWriteAudioPlay = {"source":"APIGetPost","func":"play","data":""}
_dataWriteGPIO = {"source":"APIGetPost","func":"blinkLed","data":0}


print "Start APIGetPost"
ImageBase64 = ""
IDCardNumber = ""
ftp = FTP()
ftp.set_debuglevel(2)
ftpHost = "new-thd.ddns.net"
ftpUser = "ltkftp"
ftpPass = "aNdIcKerbanDeNUmBEtIcYoFUraTHe"
ftpPath = "/files/save/in"

while True:
    waitData = getDataMqtt()
    if waitData:
        try:
            if (waitData["source"] == "MainApp") & (waitData["func"] == "recognize"):
                _dataWriteMainApp["func"] = waitData["func"]
                _dataWriteMainApp["data"] = [{"company":"","name":"","ID":"","mess":"","box": [],"score":0}]
                print "start Recognize Image!"
                FlagType = "recognize"
                _ImageBase64 = waitData["data"]["base64image"]
                FtpImage = saveImageFtp(ftpHost,ftpUser,ftpPass,ftpPath,_ImageBase64)
                if not FtpImage:
                    _dataWriteMainApp["data"][0]["mess"] = "image path is not exist!"
                    Mqtt.MqttPathPublish = "MainApp"
                    Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                    print _dataWriteMainApp
                    continue
                _timeStart = time.time()
                _respont = recognizeFaceFtp(ftpHost,ftpUser,ftpPass,FtpImage)
                _timeStop = time.time()
                if os.path.isfile('/home/pi/maychamcong/log.txt'):
                    data = open('/home/pi/maychamcong/log.txt', 'a')
                    print _timeStop-_timeStart
                    now = datetime.now()
                    data.write("RecognizeFace " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
                    data.write(str('total run-time of API in second: %fs\n\n' % (_timeStop-_timeStart)))
                    data.close()
                else:
                    print "file log.txt is not exist"
                #print _respont
                if (_respont["message"] == "SUCCESS"):
                    #print "data respont: ",_respont
                    for _numFace in range(len(_respont["data"]["result"][0]["recognition"]) - 1):
                        _dataWriteMainApp["data"].append({"company":"","name":"","ID":"","mess":"","box": [],"score":0})
                    for _numFace in range(len(_respont["data"]["result"][0]["recognition"])):
                        #_dataWriteMainApp["data"].append({"company":"","name":"","ID":"","mess":"","box": [],"score":0})
                        _score = _respont["data"]["result"][0]["recognition"][_numFace]["score"]
                        if _score == -1:
                            _dataWriteMainApp["data"][_numFace]["mess"] = _respont["data"]["result"][0]["message"] + "score = " + str("%.2f" % (_score))
                            # _dataWriteAudioPlay["data"] = u"chào bạn mời bạn đến quầy đăng ký thông tin"
                            # _dataWriteGPIO["data"] = 2
                        else:
                            _dataWriteMainApp["data"][_numFace]["mess"] = _respont["data"]["result"][0]["message"] + "score = " + str("%.2f" % (_score*100)) + "%"
                            # _dataWriteAudioPlay["data"] =  u"xin chào " + _respont["data"]["result"][0]["recognition"][0]["name"] + u" mời bạn vào"
                            # _dataWriteGPIO["data"] = 5
                        _dataWriteMainApp["data"][_numFace]["name"] = _respont["data"]["result"][0]["recognition"][_numFace]["name"]
                        _dataWriteMainApp["data"][_numFace]["company"] = userData["username"]
                        _dataWriteMainApp["data"][_numFace]["ID"] = _respont["data"]["result"][0]["recognition"][_numFace]["user_id"]
                        _dataWriteMainApp["data"][_numFace]["box"] = _respont["data"]["result"][0]["recognition"][_numFace]["box"]
                        _dataWriteMainApp["data"][_numFace]["score"] = _respont["data"]["result"][0]["recognition"][_numFace]["score"]
                else:
                    _dataWriteMainApp["data"][0]["mess"] = u"server đang gặp lỗi!"
                    # _dataWriteMainApp["data"][0]["name"] = ""
                    # _dataWriteMainApp["data"][0]["company"] = ""
                    # _dataWriteMainApp["data"][0]["ID"] = ""
                    # _dataWriteAudioPlay["data"] = u"server đang gặp lỗi"
                    # _dataWriteGPIO["data"] = 1
                
                Mqtt.MqttPathPublish = "MainApp"
                Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                # Mqtt.MqttPathPublish = "AudioPlay"
                # Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))
                # Mqtt.MqttPathPublish = "GPIO"
                # Mqtt.mqttPublish(json.dumps(_dataWriteGPIO))
                print _dataWriteMainApp

            elif (waitData["source"] == "MainApp") & (waitData["func"] == "verify"):
                print "start verify!"
                FlagType = "verify"
                _dataWriteMainApp["func"] = waitData["func"]
                _dataWriteMainApp["func"] = "verify"
                _dataWriteMainApp["data"] = {"company":"","name":"","ID":"","mess":"","box": [],"score":0}
                _ImageBase64 = waitData["data"]["base64image"]
                IDCardNumber = waitData["data"]["ID"]
                FtpImage = saveImageFtp(ftpHost,ftpUser,ftpPass,ftpPath,_ImageBase64)
                #print "start"
                if not FtpImage:
                    _dataWriteMainApp["data"]["mess"] = "image path is not exist!"
                    Mqtt.MqttPathPublish = "MainApp"
                    Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                    print _dataWriteMainApp
                    continue
                _timeStart = time.time()
                __respont = verifyFaceFtp(ftpHost,ftpUser,ftpPass,FtpImage,IDCardNumber)
                _timeStop = time.time()
                if os.path.isfile('/home/pi/maychamcong/log.txt'):
                    data = open('/home/pi/maychamcong/log.txt', 'a')
                    print _timeStop-_timeStart
                    now = datetime.now()
                    data.write("RecognizeFace " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
                    data.write(str('total run-time of API in second: %fs\n\n' % (_timeStop-_timeStart)))
                    data.close()
                else:
                    print "file log.txt is not exist"
                #print __respont
                if __respont["message"] == "SUCCESS":
                    #print __respont
                    if __respont["data"]["result"][0]["message"] == "Matched":
                    #if __respont["data"]["message"] == "Matched":
                        print IDCardNumber
                        _dataWriteGPIO["data"] = 5
                        #_dataWriteMainApp["data"]["mess"] = "Moi Ban Vao!"
                        #_dataWriteMainApp["data"]["name"] = __respont["data"]["user_data"]["user_name"]
                        _dataWriteMainApp["data"]["mess"] = "score: " + str("%.2f" % (__respont["data"]["result"][0]["score"]*100)) + u"% => Mời bạn vào!"
                        _dataWriteMainApp["data"]["name"] = __respont["data"]["result"][0]["user_data"]["user_name"]
                        _dataWriteMainApp["data"]["company"] = userData["username"]
                        _dataWriteMainApp["data"]["ID"] = IDCardNumber
                        _dataWriteAudioPlay["data"] = u"xin chào " + __respont["data"]["result"][0]["user_data"]["user_name"] + u" mời bạn vào"
                    elif __respont["data"]["result"][0]["message"] == "Not matched":
                    #if __respont["data"]["message"] == "Not matched":
                        _dataWriteGPIO["data"] = 4
                        _dataWriteMainApp["data"]["mess"] = "score: " + str("%.2f" % (__respont["data"]["result"][0]["score"]*100)) + u"% => Bạn cầm nhầm thẻ rồi!"
                        _dataWriteMainApp["data"]["name"] = ""
                        _dataWriteMainApp["data"]["company"] = ""
                        _dataWriteMainApp["data"]["ID"] = IDCardNumber
                        _dataWriteAudioPlay["data"] = u"bạn cầm nhầm thẻ rồi"
                    elif __respont["data"]["result"][0]["message"] == "there is no user presented verify id":
                    #if __respont["data"]["message"] == "there is no user presented verify id":
                        _dataWriteGPIO["data"] = 2
                        _dataWriteMainApp["data"]["mess"] = u"thẻ không hợp lệ!"
                        _dataWriteMainApp["data"]["name"] = ""
                        _dataWriteMainApp["data"]["company"] = ""
                        _dataWriteMainApp["data"]["ID"] = IDCardNumber
                        _dataWriteAudioPlay["data"] = u"thẻ không hợp lệ"
                    elif __respont["data"]["result"][0]["message"] == "There is not any face in the image":
                    #if __respont["data"]["message"] == "There is not any face in the image":
                        _dataWriteGPIO["data"] = 3
                        _dataWriteMainApp["data"]["mess"] = u"Camera chưa thấy mặt bạn!"
                        _dataWriteMainApp["data"]["name"] = ""
                        _dataWriteMainApp["data"]["company"] = ""
                        _dataWriteMainApp["data"]["ID"] = IDCardNumber
                        _dataWriteAudioPlay["data"] = u"camera chưa thấy mặt bạn"
                    else:
                        _dataWriteGPIO["data"] = 1
                        _dataWriteMainApp["data"]["mess"] = u"server gặp lỗi!"
                        _dataWriteMainApp["data"]["name"] = ""
                        _dataWriteMainApp["data"]["company"] = ""
                        _dataWriteMainApp["data"]["ID"] = IDCardNumber
                        _dataWriteAudioPlay["data"] = u"server đang gặp lỗi rồi"

                else:
                    _dataWriteMainApp["data"]["mess"] = u"server đang gặp lỗi!"
                    _dataWriteMainApp["data"]["name"] = ""
                    _dataWriteMainApp["data"]["company"] = ""
                    _dataWriteMainApp["data"]["ID"] = IDCardNumber
                    # Mqtt.MqttPathPublish = "MainApp"
                    # Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                    _dataWriteAudioPlay["data"] = u"server đang gặp lỗi rồi"
                    # Mqtt.MqttPathPublish = "AudioPlay"
                    # Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))
                    _dataWriteGPIO["data"] = 1
                    # Mqtt.MqttPathPublish = "GPIO"
                    # Mqtt.mqttPublish(json.dumps(_dataWriteGPIO))
                
                print _dataWriteMainApp
                Mqtt.MqttPathPublish = "MainApp"
                Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                Mqtt.MqttPathPublish = "GPIO"
                Mqtt.mqttPublish(json.dumps(_dataWriteGPIO))
                Mqtt.MqttPathPublish = "AudioPlay"
                Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))

            elif (waitData["source"] == "MainApp") & (waitData["func"] == "register"):
                # _dataWriteMainApp["func"] = waitData["func"]
                # _dataWriteMainApp["data"] = {"ID":"","mess":""}
                _ID = waitData["data"]["ID"]
                _userName = waitData["data"]["username"]
                _VideoBase64 = waitData["data"]["base64video"]
                _ImageBase64 = waitData["data"]["base64image"]
                _overWrite = waitData["data"]["overwrite"]
                _isPortrait = waitData["data"]["isportrait"]
                print "start register"
                _dataWriteMainAppThreadaa = {"source":"APIGetPost","func":"register","data":{"ID":"","mess":"","status":False}}
                thread = RegiterThread(_dataWriteMainAppThreadaa,_userName,_ID,_VideoBase64,_ImageBase64,_isPortrait,_overWrite)
                thread.start()
                print "exit main register!"
                # if not os.path.isfile(_VideoBase64):
                #     print "Image register path: " + _VideoBase64 + " from Mqtt is not exist"
                #     _dataWriteMainApp["data"]["mess"] = "video path is not exist!"
                #     Mqtt.MqttPathPublish = "MainApp"
                #     Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                #     print _dataWriteMainApp
                #     continue
                # videoFile = open(_VideoBase64,"rb")
                # VideoBase64 = base64.b64encode(videoFile.read())
                # videoFile.close()
                # FtpImage = saveImageFtp(ftpHost,ftpUser,ftpPass,ftpPath,_ImageBase64)
                # if FtpImage == False:
                #     _dataWriteMainApp["data"]["mess"] = "image path is not exist!"
                #     Mqtt.MqttPathPublish = "MainApp"
                #     Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
                #     print _dataWriteMainApp
                #     continue
                # #print VideoBase64
                # _timeStart = time.time()
                # _respont = registerUser(_userName,_ID,VideoBase64,_isPortrait,_overWrite)
                # _timeStop = time.time()
                # if os.path.isfile('/home/pi/maychamcong/log.txt'):
                #     data = open('/home/pi/maychamcong/log.txt', 'a')
                #     print _timeStop-_timeStart
                #     now = datetime.now()
                #     data.write("regiterUser " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
                #     data.write(str('total run-time of API in second: %fs\n\n' % (_timeStop-_timeStart)))
                #     data.close()
                # else:
                #     print "file log.txt is not exist"
                # #print _respont
                # if _respont["message"] == "SUCCESS":
                #     #print _respont
                #     _dataWriteMainApp["data"]["ID"] = _respont["data"]["user_id"]
                #     print "start verify for register!"
                #     _timeStart = time.time()
                #     __respont = verifyFaceFtp(ftpHost,ftpUser,ftpPass,FtpImage,_ID)
                #     _timeStop = time.time()
                #     if os.path.isfile('/home/pi/maychamcong/log.txt'):
                #         data = open('/home/pi/maychamcong/log.txt', 'a')
                #         print _timeStop-_timeStart
                #         now = datetime.now()
                #         data.write("verify " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
                #         data.write(str('total run-time of API in second: %fs\n\n' % (_timeStop-_timeStart)))
                #         data.close()
                #     else:
                #         print "file log.txt is not exist"
                #     if __respont["message"] == "SUCCESS":
                #         #print __respont
                #         if __respont["data"]["result"][0]["message"] == "Matched":
                #             _dataWriteMainApp["data"]["mess"] = "user is added but no training"
                #             print "start train"
                #             _timeStart = time.time()
                #             _respontRetraint = reTrainClound()
                #             _timeStop = time.time()
                #             if os.path.isfile('/home/pi/maychamcong/log.txt'):
                #                 data = open('/home/pi/maychamcong/log.txt', 'a')
                #                 print _timeStop-_timeStart
                #                 now = datetime.now()
                #                 data.write("retrain cloud API" + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
                #                 data.write(str('total run-time of API in second: %fs\n\n' % (_timeStop-_timeStart)))
                #                 data.close()
                #             else:
                #                 print "file log.txt is not exist"
                #             if _respontRetraint["message"] == "SUCCESS":
                #                 print "retrain success clound"
                #                 _dataWriteMainApp["data"]["mess"] = "user is added and ready to use"
                #             else:
                #                 print _respontRetraint
                #         else:
                #             print "image and video is not 1 people!"
                #             _dataWriteMainApp["data"]["mess"] = "user is not math with video"
                #     else:
                #         print __respont
                #         print "can't verify image!"
                #         _dataWriteMainApp["data"]["mess"] = "can not verify image with user"
                # else:
                #     print _respont
                #     print "can't register user!"
                #     _dataWriteMainApp["data"]["mess"] = "can not register,maybe video to large"

                # print _dataWriteMainApp
                # Mqtt.MqttPathPublish = "MainApp"
                # Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
            
            elif (waitData["source"] == "MainApp") & (waitData["func"] == "getalluser"):
                print "start get all user in database!"
                _dataWriteMainApp["func"] = waitData["func"]
                _dataWriteMainApp["data"] = [{"address":"","total_faces":0,"pid":"","name":"","ID":"","mess":""}]
                _timeStart = time.time()
                _respont = getAllUsers(5)
                _timeStop = time.time()
                if os.path.isfile('/home/pi/maychamcong/log.txt'):
                    data = open('/home/pi/maychamcong/log.txt', 'a')
                    print _timeStop-_timeStart
                    now = datetime.now()
                    data.write("get all data user " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
                    data.write(str('total run-time of API in second: %fs\n\n' % (_timeStop-_timeStart)))
                    data.close()
                else:
                    print "file log.txt is not exist"
                if _respont["message"] == "SUCCESS":
                    #Sprint _respont
                    for _data in range(len(_respont["data"]["result"]) - 1):
                        _dataWriteMainApp["data"].append({"address":"","total_faces":0,"pid":"","name":"","ID":"","mess":""})
                    for _data in range(len(_respont["data"]["result"])):
                        #_dataWriteMainApp["data"].append({"address":"","total_faces":0,"pid":"","name":"","ID":"","mess":""})
                        _dataWriteMainApp["data"][_data]["address"] = _respont["data"]["result"][_data]["address"]
                        _dataWriteMainApp["data"][_data]["ID"] = _respont["data"]["result"][_data]["id"]
                        _dataWriteMainApp["data"][_data]["name"] = _respont["data"]["result"][_data]["name"]
                        _dataWriteMainApp["data"][_data]["total_faces"] = _respont["data"]["result"][_data]["total_faces"]
                else:
                    _dataWriteMainApp["data"][0]["mess"] = "fails to get all user data!"
                    print "get all user fails!"
                    print _respont

                print _dataWriteMainApp
                Mqtt.MqttPathPublish = "MainApp"
                Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))

            elif (waitData["source"] == "MainApp") & (waitData["func"] == "deleteuser"):
                _ID = waitData["data"]["ID"]
                _dataWriteMainApp["func"] = waitData["func"]
                _dataWriteMainApp["data"] = {"ID":"","mess":""}
                print "start delete user", _ID                
                _timeStart = time.time()
                _respont = deleteUser(_ID)
                print _respont
                _timeStop = time.time()
                if os.path.isfile('/home/pi/maychamcong/log.txt'):
                    data = open('/home/pi/maychamcong/log.txt', 'a')
                    print _timeStop-_timeStart
                    now = datetime.now()
                    data.write("get all data user " + str(now.strftime("%m/%d/%Y, %H:%M:%S:\n")))
                    data.write(str('total run-time of API in second: %fs\n\n' % (_timeStop-_timeStart)))
                    data.close()
                else:
                    print "file log.txt is not exist"
                if _respont["message"] == "SUCCESS":
                    if _respont["data"]["result"]:
                        _dataWriteMainApp["data"]["ID"] = _ID
                        _dataWriteMainApp["data"]["mess"] = ""
                    else:
                        _dataWriteMainApp["data"]["mess"] = "there are no user in id: ", _ID
                else:
                    _dataWriteMainApp["data"]["mess"] = "fails get delete user"

                print _dataWriteMainApp
                Mqtt.MqttPathPublish = "MainApp"
                Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))

            else:
                print waitData
                print "MQTT data error: source or func is not true!"
        except Exception as e:
            print "MQTT data error: ", e
    else:
        continue

