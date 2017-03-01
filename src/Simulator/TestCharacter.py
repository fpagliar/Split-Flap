from DisplayFactory import DisplayFactory
import Pin
from Configuration import defaultSystemConfiguration, defaultSystemStatus, Keywords
import time
from Logger import debug

if __name__ == "__main__":
  config = defaultSystemConfiguration()
  display = DisplayFactory(Pin.GetTextPin, config, defaultSystemStatus()).buildCharacterTester()
  debug()
  for char in config.get(Keywords.CHARACTERS_ARRAY):
    display.show(char)
    time.sleep(5)
