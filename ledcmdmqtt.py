import random
import sys
import time
from datetime import datetime

from Adafruit_IO import MQTTClient

import RPi.GPIO as GPIO

# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY      = 'your aio_key'
ADAFRUIT_IO_USERNAME = 'your username'

#setup GPIO
led_2 = 25
led_3 = 24
led_8 = 27


# Define callback functions which will be called when certain events happen.
def connected(client):
  #print 'MQTT Connected to Adafruit IO!  Listening for feed changes... ', str(datetime.now())
  client.subscribe('led2command')
  client.subscribe('led3command')
  client.subscribe('led8command')

def disconnected(client):
  time.sleep(3)
  try:
    client.connect()
    client.loop_background()
  except:
    print 'Disconnected to Adafruit IO (MQTT)! ', time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime())
    sys.exit(1)

def getLED(feed):
  if (feed == 'led2command'):
    return led_2
  elif (feed == 'led3command'):
    return led_3
  elif (feed == 'led8command'):
    return led_8
  return None

def switchLED(val, led):
  if (val == 'ON'):
    GPIO.output(led, GPIO.HIGH)
  elif (val == 'OFF'):
    GPIO.output(led, GPIO.LOW)
  


def message(client, feed_id, payload):
  feed = format(feed_id)
  val = format(payload)
  led = getLED(feed)
  if (led is not None):
    switchLED(val, led)

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.

def init():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(led_2, GPIO.OUT)
  GPIO.output(led_2, GPIO.LOW)
  GPIO.setup(led_3, GPIO.OUT)
  GPIO.output(led_3, GPIO.LOW)
  GPIO.setup(led_8, GPIO.OUT)
  GPIO.output(led_8, GPIO.LOW)
  client.connect()
  client.loop_background()

def run():
  while True:
    try:
      #do what you want!
      time.sleep(10)
    except KeyboardInterrupt:
      sys.exit(1)

if __name__ == '__main__':
  init()
  run()

