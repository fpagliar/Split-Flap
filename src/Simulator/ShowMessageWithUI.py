from SplitFlapGUI import SplitFlapGUI
from DisplayFactory import DisplayFactory
import Pin
from Configuration import defaultSystemConfiguration, defaultSystemStatus
from MessageRequester import MessageRequester
from threading import Thread

if __name__ == "__main__":
  config = defaultSystemConfiguration()
  gui = SplitFlapGUI(config)
  display = DisplayFactory(lambda x: Pin.GetLoggerPin(x, gui), config, defaultSystemStatus()).build()
  gui.setDisplay(display)
  with open("messages.log", "a") as log:
    with open("messages.txt", "a") as feed:    
      thread = Thread(target = MessageRequester(feed, log, display).start)
      thread.start()
  gui.run()
