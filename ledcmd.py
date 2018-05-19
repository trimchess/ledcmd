from Adafruit_IO import Client
import time
import adafruitkey

aio = None

def sendFeed(self,ledFeed):
  val = getFeedState(self,ledFeed)
  if (val == 'ON'):
    cmd = 'OFF'
  elif (val == 'OFF'):
    cmd = 'ON'
  try:
    aio.send(ledFeed,cmd)
  except:
    return

def getFeedState(self,ledFeed):
  global aio
  try:  
    data = aio.receive(ledFeed)
  except:
    try:
      aio = Client(adafruitkey.ADAFRUIT_IO_KEY)
      data = aio.receive(ledFeed)
    except:   
      return None
  return str(data.value)



