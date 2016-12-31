from SplitFlapGUI import SplitFlapGUI
from DisplayFactory import DisplayFactory
import Pin
from Configuration import defaultSystemConfiguration, defaultSystemStatus

if __name__ == "__main__":
  config = defaultSystemConfiguration()
  gui = SplitFlapGUI(config)
  display = DisplayFactory(lambda x: Pin.GetLoggerPin(x, gui), config, defaultSystemStatus()).build()
  gui.setDisplay(display)
  gui.run()
