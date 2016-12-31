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
      while not Utils.askForConfirmation("Is it showing letter B now?"):
        controller.tick(i)
      systemStatus.set(i, 0, self._config.CHARACTERS_ARRAY.index('B'), controller.getSequence(1).currentIndex())
#       print("Let me first turn in order to get the sequence to the start point")
#       for _ in range(len(self._config.MOTOR_SEQUENCE) + 1):
#         controller.tick(i)
#       currSequence = 0
#       print("Now, we will try to configure the ticks to zero")
#       letterIndex = Utils.askForOption("What letter is it showing now?", self._config.CHARACTERS_ARRAY)
#       while not Utils.askForConfirmation("Is it showing letter " + self._config.CHARACTERS_ARRAY[letterIndex + 1] + " now?"):
#         currSequence += 1
#         controller.tick(i)
      # Ticks is now at 0. What we want, is to send the whole sequence of 
#       systemStatus.set(i, 0, letterIndex + 1, currSequence)
    systemStatus.save()
    print("Great, now the split-flap is correctly configured")
    
  def _createPinsFromIds(self, ids):
    return [self._pinBuilder(ids[i]) for i in range(len(ids))]    
  
  def _sequenceBuilder(self):
    return MotorSequence(self._createPinsFromIds(self._config.SEQUENCE_PINS), self._config.MOTOR_SEQUENCE)
