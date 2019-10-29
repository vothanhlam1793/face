#!/usr/bin/python
# -*- coding: utf8 -*-
#!/usr/bin/python

import Queue
import threading
import time
import paho.mqtt.client as mqtt

class MQTTClient (object):
    MqttServer = "11.12.13.147"
    MqttPathSubcribe = "test_channel"
    MqttPathPublish = "test_channel"
    MqttPort = 1883
    DataSubcribe = Queue.Queue(10)

    # The callback for when the client receives a CONNA$
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.MqttPathSubcribe)

    # The callback for when a PUBLISH message is receiv$
    def on_message(self,client, userdata, msg):
        #print(msg.topic+" "+str(msg.payload))
        self.DataSubcribe.put(msg.payload)

    def mqttSubcribe(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.MqttServer, self.MqttPort, 60)
        client.loop_forever()

    def getData(self):
        if not self.DataSubcribe.empty():
            #self.queueLock.acquire()
            data = self.DataSubcribe.get()
            #self.queueLock.release()
            #print "data read: ", data
            return data

    def mqttPublish(self, _mess):
	client = mqtt.Client()
	client.connect(self.MqttServer, self.MqttPort, 60)
	client.publish(self.MqttPathPublish, _mess)
