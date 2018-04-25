import smbus
import os
import sys
import urllib.request, urllib.parse, urllib.error
import requests
import spidev
import time
import os
import subprocess
import json

################# Default Constants #################
# These can be changed if required
DEVICE        = 0x77 # Default device I2C address
THINGSPEAKKEY = '7XG54V0FZLMGGVSZ'
THINGSPEAKURL = 'https://api.thingspeak.com/update'
CHANNEL_ID=481094
READ_API_KEY='8VN2B2SSQ235HMW9G'

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def sendData(url,key,field1,field2,temp,light):
  """
  Send event to internet site
  """
  response = urllib.request.urlopen('https://api.thingspeak.com/update?api_key=%s&field1=%s&field2=%s' % (THINGSPEAKKEY, temp, light))
  print(response)
  response.close()
        

def ReadChannel(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data

def ConvertVolts(data,places):
	volts = (data * 3.3) / float(1023)
	volts = round(volts,places)
	return volts

def ConvertTemp(data,places):
	temp = ((data * 330)/float(1023))-50
	temp = round(temp,places)
	temp = (temp*(9/5)) + 32
	return temp

light_channel = 0
temp_channel = 1

delay = 27

while True:

        light_level = ReadChannel(light_channel)
        light_volts = ConvertVolts(light_level,2)

	
        temp_level = ReadChannel(temp_channel)
        temp_volts = ConvertVolts(temp_level,2)
        temp = ConvertTemp(temp_level,2)

        print("-------------------------------------")
        print(("Light: {} ({}V)".format(light_level,light_volts)))
        print(("Temp: {} ({}V) {} deg F".format(temp_level,temp_volts,temp)))
	
        process = subprocess.Popen(["./main", "blockchain.txt", str(light_level), str(temp)], stdout=subprocess.PIPE)
        process.wait()
	
        for line in process.stdout:
            print(line)
            
        sendData(THINGSPEAKURL,THINGSPEAKKEY,'Temp','Light',temp, light_level)
        
        conn = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key%s" \
                                % (CHANNEL_ID, READ_API_KEY))
        response = conn.read()
        data = json.loads(response.decode('ascii'))
        conn.close()

        if data['field3'] == '1':
            t = 'Fan-on'
        else:
            t = 'Fan-off'
        
        if data['field4'] == '1':
            l = 'Light-on ' + data['created_at']
        else:
            l = 'Light-off ' + data['created_at']
        process = subprocess.Popen(["./main", "blockchain.txt", t, l], stdout=subprocess.PIPE)
        process.wait()
        
        for line in process.stdout:
            print(line)
        
        time.sleep(delay)
