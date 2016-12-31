from DisplayFactory import DisplayFactory
import Pin
from Configuration import defaultSystemConfiguration, defaultSystemStatus

if __name__ == "__main__":
  display = DisplayFactory(Pin.GetPin, defaultSystemConfiguration(), defaultSystemStatus()).build()
  display.show("ABCDEFGH")
