from SplitFlapGUI import SplitFlapGUI
from DisplayFactory import DisplayFactory
import TextBasedPin

if __name__ == "__main__":
  display = DisplayFactory(TextBasedPin.GetPin).build()
  SplitFlapGUI(display).run()
