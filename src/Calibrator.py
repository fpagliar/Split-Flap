from DisplayFactory import DisplayFactory
from Logger import log
import Utils
import time
from Configuration import SystemCalibration, SystemStatus

# This class takes care of the calibration of each character.
# calibrateInitialPosition will help us set the start position of the system. This is the way the program will be able to
# know which letter it is showing at the moment, what step is the motor sequence in, and how many steps till the next letter shows.
# Once you calibrate the initial position, it will be saved to a file and there is not need to set it again unless something bad happens
# The other part is calibrateTicksPerLetter, and this will save which is the composition of the characters and the physical system
# and will be saved and shouldn't be run again unless you change/replace a character.
class Calibrator:
  def __init__(self, pinBuilder, config):
    self._pinBuilder = pinBuilder
    self._config = config

  def infiniteRun(self):
    controller = _CalibratorCharacter(self._pinBuilder, 1, self._config)
    while True:
      controller.tick()
      time.sleep(0.001)

  def calibrateTicksPerLetter(self):
    self.calibrateInitialPosition()
    numberOfMotors = self._config.numberOfMotors()
    controller = _CalibratorCharacter(self._pinBuilder, numberOfMotors, self._config)
    calibration = SystemCalibration()
    alphabet = self._config.alphabet()

    for i in range (1, numberOfMotors + 1):
      print("Now calibrating the character " + str(i))
      ticksConfiguration = []
      ticks = 0
      for letter in alphabet[:1]:  # We start with A showing, so the next letter should be the first target
        while not Utils.askForConfirmation("Is it showing character " + letter + "?", 0.5):
          controller.tick(i - 1)
          ticks = ticks + 1
        ticksConfiguration.append(ticks)
      calibration.set(i, ticksConfiguration)
    print("Great, calibration ended")
    calibration.save()

  def calibrateInitialPosition(self):
    numberOfMotors = self._config.numberOfMotors()
    controller = _CalibratorCharacter(self._pinBuilder, numberOfMotors, self._config)
    systemStatus = SystemStatus()
    systemStatus.cleanup()
    target = self._config.alphabet()[0]

    for i in range (1, numberOfMotors + 1):
      print("Now configuring the character " + str(i))
      while not Utils.askForConfirmation("Is it close to " + target + "?", 0.05):
        controller.tick(i - 1)
      while not Utils.askForConfirmation("Is it showing letter " + target + "?", 0.5):
        controller.tick(i - 1)
      systemStatus.set(i, 0, controller.getSequence().currentIndex())
    systemStatus.save()
    print("Great, now the split-flap is correctly configured")

class _CalibratorCharacter:
  def __init__(self, pinBuilder, quantity, config):
    factory = DisplayFactory(pinBuilder, config, SystemStatus(quantity))
    self._sequences, self._connection = factory.buildCharacterCalibrator(quantity)

  def getSequences(self):
    return self._sequences

  def tick(self, index):
    self._sequences[index].next()
    self._connection.publish()
