#Acts based on infomation recieved from another pi
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)

import urllib.request,json
READ_API_KEY='8VN2BSSQ235HMW9G'
CHANNEL_ID=481094
THINGSPEAKKEY = '7XG54V0FZLMGGVSZ'
THINGSPEAKURL = 'https://api.thingspeak.com/update'

def sendData(url, key, field3, field4, tempOn, lightOn):
    response = urllib.request.urlopen('https://api.thingspeak.com/update?api_key=%s&field3=%s&field4=%s' % (THINGSPEAKKEY, tempOn, lightOn))
    print(response)
    response.close()
    #time.sleep(10)
####def main():

lightOn = 0
tempOn = 0
while True:
    '''
    conn = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                                % (CHANNEL_ID,READ_API_KEY))
    response = conn.read()
    print "http status code=%s" % (conn.getcode())
    data=json.loads(response)
    print data['field1'],data['field2'],data['created_at']
    conn.close()
    '''
    
    
    conn = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (CHANNEL_ID,READ_API_KEY))
    response = conn.read()
    print("http status code=%s" % (conn.getcode()))
    data=json.loads(response.decode('ascii'))
    print(data['field1'],data['field2'],data['created_at'])
    conn.close()
    
    if data['field1'] != None:
        temperature = float(data['field1'])
        uTemp = 70 
        if uTemp < temperature:
            GPIO.output(24,GPIO.HIGH)
            tempOn = 1
        else:
            GPIO.output(24,GPIO.LOW)
            tempOn = 0
            
    if data['field2'] != None:
        light = float(data['field2'])
        uLight = 530       
        if light > uLight:
            GPIO.output(18,GPIO.HIGH)
            lightOn = 1
        else:
            GPIO.output(18,GPIO.LOW)
            lightOn = 0
    #time.sleep(10)

    sendData(THINGSPEAKURL, THINGSPEAKKEY, 'Temp', 'Light', tempOn, lightOn)        

    time.sleep(30)
#except KeyboardInterrupt:
    #print("Exiting...")

    
#finally:
   # GPIO.cleanup()
