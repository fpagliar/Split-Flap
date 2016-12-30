from MotorController import MotorController
from MotorCommunicator import MotorCommunicator
from Multiplexor import Multiplexor
from Configuration import defaultConfiguration
from MotorSequence import MotorSequence
import Utils

class Calibrator:
  def __init__(self, pinBuilder):
    self._pinBuilder = pinBuilder
    self._config = defaultConfiguration()
    self._config.load()
    
  def setupController(self, motors):
    multiplexorPins = self._createPinsFromIds(self._config.MULTIPLEXER_PINS)
    powerPin = self._pinBuilder(self._config.MULTIPLEXER_POWER_PIN)
    multiplexor = Multiplexor(multiplexorPins, powerPin)    
    return MotorController(motors, MotorCommunicator(multiplexor), self.sequenceBuilder)
    
  def calibrateTicksPerLetter(self):
    controller = self.setupController(1)
    print("Please take a look at the first character, we will need to validate when the letter is changed for setup")
    while not Utils.askForConfirmation("Is it showing the next letter now?"):
      controller.tick(1)
    
    print("Great, now we will count the number of turns until the letter changes again")

    ticks = 0
    while not Utils.askForConfirmation("Is it showing the next letter now?"):
      controller.tick(1)
      ticks = ticks + 1
    print("Great, it takes " + str(ticks) + " turns to change a letter")
    self._config.TICKS_PER_LETTER = ticks
    self._config.save()

  def calibrateInitialPosition(self):
    controller = self.setupController(self._config.NUMBER_OF_MOTORS)
    print("Please spin all the flaps to show the letter A")
    for i in range (self._config.NUMBER_OF_MOTORS):
      print("Now configuring the character " + str(i + 1))
      while not Utils.askForConfirmation("Is it showing letter B now?"):
        controller.tick(i)
    print("Great, now the split-flap is correctly configured")
  
  def _createPinsFromIds(self, ids):
    return [self._pinBuilder(ids[i]) for i in range(len(ids))]    
  
  def sequenceBuilder(self):
    return MotorSequence(self._createPinsFromIds(self._config.SEQUENCE_PINS), self._config.MOTOR_SEQUENCE)
