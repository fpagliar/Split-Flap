import sys
import Pin
import time
from Calibrator import Calibrator
from DisplayFactory import DisplayFactory
from Configuration import SystemConfiguration, SystemStatus
import re

option = None
if len(sys.argv) > 1:
  option = sys.argv[1]
config = SystemConfiguration()

if option == "--position":
    calibrator = Calibrator(Pin.GetPin, config)
    calibrator.calibrateInitialPosition()
elif option == "--ticks":
    calibrator = Calibrator(Pin.GetPin, config)
    calibrator.calibrateTicksPerLetter()
elif option == "--message":
    display = DisplayFactory(Pin.GetPin, config, SystemStatus(config.numberOfMotors())).build()
    display.show(sys.argv[2])
elif option == "--show":
    display = DisplayFactory(Pin.GetPin, config, SystemStatus(config.numberOfMotors())).buildCharacterTester()
    while True:
        display.show(input("What do you want to show next?"))
elif option == "--character":
    display = DisplayFactory(Pin.GetPin, config, SystemStatus(config.numberOfMotors())).buildCharacterTester()
    for char in config.alphabet():
        display.show(char)
        time.sleep(5)
elif option == "--infinite":
    calibrator = Calibrator(Pin.GetPin, config)
    calibrator.infiniteRun()
elif option == "--shift-registry":
    length = 0
    while length <= 0:
      answer = input("Enter the desired length of the shift registry: ")
      if answer.isdigit():
        length = int(answer)
    registry = DisplayFactory(Pin.GetPin, config, SystemStatus(length)).buildShiftRegistry(length)
    regex = re.compile("[01]{" + str(length) + "}")
    while True:
      pattern = input("What do you want to show?")
      if regex.match(pattern) is None:
        print("Invalid input: " + pattern)
      else:
        binary = [x == "1" for x in pattern]
        registry.set(binary)

else:
  print("Valid options: \n \t --position \n \t --ticks \n \t --message \n \t --show \n \t --character \n \t --infinite \n \t --shift-registry \n")

