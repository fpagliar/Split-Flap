import sys
import Pin
import time
from Calibrator import Calibrator
from DisplayFactory import DisplayFactory
from Configuration import defaultSystemConfiguration, defaultSystemStatus, Keywords

option = sys.argv[1]

if option == "--position":
    calibrator = Calibrator(Pin.GetPin)
    calibrator.calibrateInitialPosition()
elif option == "--ticks":
    calibrator = Calibrator(Pin.GetPin)
    calibrator.calibrateTicksPerLetter()
elif option == "--message":
    display = DisplayFactory(Pin.GetPin, defaultSystemConfiguration(), defaultSystemStatus()).build()
    display.show(sys.argv[2])
elif option == "--show":
    display = DisplayFactory(Pin.GetPin, defaultSystemConfiguration(), defaultSystemStatus()).buildCharacterTester()
    while True:
        display.show(input("What do you want to show next?"))
elif option == "--character":
    config = defaultSystemConfiguration()
    display = DisplayFactory(Pin.GetPin, config, defaultSystemStatus()).buildCharacterTester()
    for char in config.get(Keywords.CHARACTERS_ARRAY):
        display.show(char)
        time.sleep(5)
elif option == "--infinite":
    calibrator = Calibrator(Pin.GetPin)
    calibrator.infiniteRun()
elif option == "--config":
    defaultSystemConfiguration().save()
else:
    raise Exception("Invalid option")


