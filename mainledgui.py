from Tkinter import *
from Tkinter import Menu
import ledcmd as ledcmd
import ledmqttsubs as mqtt

class GUI(Frame):
  """GUI Frame"""
  def __init__(self):
    """Constructor"""
    self.root = Tk()
    self.root.title("LED Control")
    self.root.resizable(0,0)
    Frame.__init__(self, self.root)
    self.empty = LabelFrame(self.root)
    self.empty.grid()
    self.buttonContainer = LabelFrame(self.root, text=' Control Buttons for LED 1 - 8 ')
    self.buttonContainer.grid()
    self.createMenu()
    self.createWidgets(self.root)
    

  def on_buttonClick(self,event):
    """Eventhandler"""
    """Sends data to the Adafruit IO system and updates the GUI (colour of command buttons)"""
    feedOfButton = event.widget.feed
    ledcmd.sendFeed(self, feedOfButton)

  def on_quit(self):
    """Quit program."""
    quit()

  def setButtonColorOfState(self,ledButton,feed):
    """Switches the state of a button depending on the actuel feed state"""
    """ON, OFF, undefined"""
    state = ledcmd.getFeedState(self, feed)
    self.buttonColorHandler(state, ledButton)
    
  def setAllButtonColorOfState(self):
    """Switches the state of a button depending on the actuel feed state"""
    """Mainly used to update buttons"""
    for feed in self.buttonFeedList:
      self.setButtonColorOfState(self.dict[feed], feed) 
      
  def updateButton(self, feed, state):
    """Translates a feed to a button and actualize its colour"""
    """Used to update Buttoncolours when subscribed feeds fire an change event"""
    ledButton = self.dict[feed]
    self.buttonColorHandler(state, ledButton)
  
  
  def buttonColorHandler(self, state, button):
    """Actualize the colour of a button depending on its state"""
    if(state == 'ON'):
      button.configure(bg = "green")
    elif(state == 'OFF'):
      button.configure(bg = "red")
    else:
      button.configure(bg = "grey")
  
  def createMenu(self):
    """Create the menu bar"""
    menuBar = Menu(self.root)
    self.root.config(menu=menuBar)
    fileMenu = Menu(menuBar, tearoff=0)
    fileMenu.add_command(label="Exit", command=self.on_quit)
    menuBar.add_cascade(label="File", menu=fileMenu)

      
  def createWidgets(self,master):
    """Helper to create the widgets and the layout"""
    self.buttonFeedList = ('led1command', 'led2command', 'led3command', 'led4command',
                          'led5command', 'led6command', 'led7command', 'led8command')
    w = 12
    h = 4
    b = 4
    """Create buttons and make association to the corresponding feed""" 
    self.ledbutton_1 = Button(self.buttonContainer, text="LED 1", width = w, height = h, bd = b)
    self.ledbutton_1.feed = self.buttonFeedList[0]
    self.ledbutton_2 = Button(self.buttonContainer, text="LED 2", width = w, height = h, bd = b)
    self.ledbutton_2.feed = self.buttonFeedList[1]
    self.ledbutton_3 = Button(self.buttonContainer, text="LED 3", width = w, height = h, bd = b)
    self.ledbutton_3.feed = self.buttonFeedList[2]
    self.ledbutton_4 = Button(self.buttonContainer, text="LED 4", width = w, height = h, bd = b)
    self.ledbutton_4.feed = self.buttonFeedList[3]
    self.ledbutton_5 = Button(self.buttonContainer, text="LED 5", width = w, height = h, bd = b)
    self.ledbutton_5.feed = self.buttonFeedList[4]
    self.ledbutton_6 = Button(self.buttonContainer, text="LED 6", width = w, height = h, bd = b)
    self.ledbutton_6.feed = self.buttonFeedList[5]
    self.ledbutton_7 = Button(self.buttonContainer, text="LED 7", width = w, height = h, bd = b)
    self.ledbutton_7.feed = self.buttonFeedList[6]
    self.ledbutton_8 = Button(self.buttonContainer, text="LED 8", width = w, height = h, bd = b)
    self.ledbutton_8.feed = self.buttonFeedList[7]

    """dictionary for feed/button association and access""" 
    self.dict = {self.ledbutton_1.feed:self.ledbutton_1,
                 self.ledbutton_2.feed:self.ledbutton_2,
                 self.ledbutton_3.feed:self.ledbutton_3,
                 self.ledbutton_4.feed:self.ledbutton_4,
                 self.ledbutton_5.feed:self.ledbutton_5,
                 self.ledbutton_6.feed:self.ledbutton_6,
                 self.ledbutton_7.feed:self.ledbutton_7,
                 self.ledbutton_8.feed:self.ledbutton_8}  
    """key binding. Associate click event to left mouse button"""
    for feed in self.buttonFeedList:
      self.dict[feed].bind("<Button-1>", self.on_buttonClick)
    
      
    """Layout"""
    c = 1
    r = 1    
    for bt in self.buttonFeedList:
      self.dict[bt].grid(row=r, column=c, sticky=W)
      c += 1
      if (c == 5):
        c = 1
        r += 1

    """init button colors depending on the feed state"""
    self.setAllButtonColorOfState()

if __name__ == "__main__":
  gui = GUI()
  mqtt.init(gui)
  mqtt.run() 
  gui.mainloop()
