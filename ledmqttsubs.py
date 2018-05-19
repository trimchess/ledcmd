import sys
import time
from datetime import datetime
from Adafruit_IO import MQTTClient
import mainledgui
import adafruitkey

# Define callback functions which will be called when certain events happen.
# adapt the subscritions for each new button
def connected(client):
  #print('MQTT Connected to Adafruit IO!  Listening for feed changes... ', str(datetime.now()))
  #client.subscribe('led1command')
  client.subscribe('led2command')
  client.subscribe('led3command')
  #client.subscribe('led4command')
  #client.subscribe('led5command')
  #client.subscribe('led6command')
  #client.subscribe('led7command')
  client.subscribe('led8command')

def disconnected(client):
  time.sleep(3)
  try:
    client.connect()
    client.loop_background()
  except:
    print 'Disconnected to Adafruit IO (MQTT)! ', time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime())
    sys.exit(1)

def message(client, feed_id, payload):
  feed = format(feed_id)
  val = format(payload)
  theGui.updateButton(feed, val)
   
# Create an MQTT client instance.
client = MQTTClient(adafruitkey.ADAFRUIT_IO_USERNAME, adafruitkey.ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
def init(gui):
  global theGui
  theGui = gui
  client.connect()  
  
def run():
  client.loop_background()  
  
