from MotorController import MotorController
from MotorCommunicator import MotorCommunicator
from Multiplexor import Multiplexor
from Configuration import defaultSystemConfiguration, cleanSystemStatus
from MotorSequence import MotorSequence
import Utils

class Calibrator:
  def __init__(self, pinBuilder):
    self._pinBuilder = pinBuilder
    self._config = defaultSystemConfiguration()
    self._config.load()
    
  def setupController(self, motors):
    multiplexorPins = self._createPinsFromIds(self._config.MULTIPLEXER_PINS)
    powerPin = self._pinBuilder(self._config.MULTIPLEXER_POWER_PIN)
    multiplexor = Multiplexor(multiplexorPins, powerPin)    
    return MotorController(MotorCommunicator(multiplexor), [self._sequenceBuilder() for _ in range(motors)])
    
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
    systemStatus = cleanSystemStatus()
    systemStatus.cleanup()
    print("Please spin all the flaps to show the letter A")
    for i in range (1, self._config.NUMBER_OF_MOTORS + 1):
      print("Now configuring the character " + str(i))
      # This will help us take the ticks variable to zero (first appearance of the letter = 0)
      # Plus it will also configure our sequence to execute correctly (if the motor is waiting for 
      # sequence 5 and we start from zero, it will ignore our calls 0-4, and start turning from 5 onwards.
      while not Utils.askForConfirmation("Is it showing letter B now?"):
        controller.tick(i)
      systemStatus.set(i, 0, self._config.CHARACTERS_ARRAY.index('B'), controller.getSequence(1).currentIndex())
    systemStatus.save()
    print("Great, now the split-flap is correctly configured")
    
  def _createPinsFromIds(self, ids):
    return [self._pinBuilder(ids[i]) for i in range(len(ids))]    
  
  def _sequenceBuilder(self):
    return MotorSequence(self._createPinsFromIds(self._config.SEQUENCE_PINS), self._config.MOTOR_SEQUENCE)
