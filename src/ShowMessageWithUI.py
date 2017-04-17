from SplitFlapGUI import SplitFlapGUI
from DisplayFactory import DisplayFactory
import Pin
from Configuration import defaultSystemConfiguration, defaultSystemStatus
from MessageRequester import MessageRequester
from threading import Thread

class createMessageRequester:
  def __init__(self, display):
    self._display = display
  
  def run(self):  
    with open("messages.log", "a") as log:
      with open("messages.txt", "r+") as feed:    
        MessageRequester(feed, log, display).start()

if __name__ == "__main__":
  config = defaultSystemConfiguration()
  gui = SplitFlapGUI(config)
  display = DisplayFactory(lambda x: Pin.GetLoggerPin(x, gui), config, defaultSystemStatus()).build()
  gui.setDisplay(display)
  messageReq = createMessageRequester(display)
  thread = Thread(target = messageReq.run)
  thread.start()
  gui.run()
