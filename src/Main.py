import sys
import Pin
import time

from Calibrator import Calibrator
from DisplayFactory import DisplayFactory
from Configuration import SystemConfiguration, SystemStatus
import re
from Configuration import SystemCalibration

# TODO:
# 3 - Make character show the middle of the array instead of the first letter
# 8 - Fix the building of the standard display by using the calibration file.
# 9 - Offer slow calibration of characters.
# 10 - DisplayFactory and Calibrator methods need some tidying up.
# 11 - Calibrate copy value to others in the array
# 12 - Figure out different run modes for windows and raspi

option = None
if len(sys.argv) > 1:
  option = sys.argv[1]
config = SystemConfiguration()

if option == "--position":
    calibrator = Calibrator(Pin.GetPin, config)
    calibrator.calibrateInitialPosition()
elif option == "--fine-tuning":
    calibrator = Calibrator(Pin.GetPin, config)
    calibrator.calibrateInitialPosition()
    calibrator.calibrateTicksPerLetter(SystemStatus(config.numberOfMotors()), SystemCalibration(config.numberOfMotors()))
elif option == "--recalibrate":
    calibrator = Calibrator(Pin.GetPin, config)
    calibrator.calibrateInitialPosition()
    systemCalibration = SystemCalibration(config.numberOfMotors())
    systemCalibration.cleanup()
    calibrator.calibrateTicksPerLetter(SystemStatus(config.numberOfMotors()), systemCalibration)
elif option == "--message":
    display = DisplayFactory(Pin.GetPin, config).build(SystemStatus(config.numberOfMotors()))
    display.show(sys.argv[2])
elif option == "--show":
    display = DisplayFactory(Pin.GetPin, config).buildDisplay(SystemStatus(config.numberOfMotors()), SystemCalibration(config.numberOfMotors()))
    while True:
	for letter in raw_input("What do you want to show next?"):
		display.show(letter)
		time.sleep(2)
	time.sleep(10)
        #display.show(raw_input("What do you want to show next?"))
elif option == "--character":
    display = DisplayFactory(Pin.GetPin, config).buildDisplay(SystemStatus(1))
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
      #if answer.isdigit():
      length = int(answer)
    registry = DisplayFactory(Pin.GetPin, config).buildShiftRegistry(length)
    regex = re.compile("[01]{" + str(length) + "}")
    while True:
      pattern = raw_input("What do you want to show?")
      if regex.match(pattern) is None:
        print("Invalid input: " + pattern)
      else:
        binary = [x == "1" for x in pattern]
        registry.set(binary)

else:
  print("Valid options: \n \t --position \n \t --fine-tuning \n \t --recalibrate \n \t --message \n \t --show \n \t --character \n \t --infinite \n \t --shift-registry \n")

