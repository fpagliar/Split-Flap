from Configuration import defaultSystemConfiguration, cleanSystemStatus
from DisplayFactory import DisplayFactory
from Configuration import Keywords
import Utils
import time

class Calibrator:
  def __init__(self, pinBuilder):
    self._pinBuilder = pinBuilder
    self._config = defaultSystemConfiguration()
    self._config.load()

  def infiniteRun(self):
    controller = CalibratorCharacter(self._pinBuilder)
    while True:
      controller.tick()
      time.sleep(0.001)
        
  def calibrateTicksPerLetter(self):
    controller = CalibratorCharacter(self._pinBuilder)
    print("Please take a look at the first character, we will need to validate when the letter is changed for setup")
    while not Utils.askForConfirmation("Is it showing the next letter now?"):
      controller.tick()
    
    print("Great, now we will count the number of turns until the letter changes again")

    ticks = 0
    while not Utils.askForConfirmation("Is it showing the next letter now?"):
      controller.tick()
      ticks = ticks + 1
    print("Great, it takes " + str(ticks) + " turns to change a letter")
    self._config.setTicksPerLetter(ticks)
    self._config.save()

  def calibrateInitialPosition(self):
    controller = CalibratorCharacter(self._pinBuilder)
    systemStatus = cleanSystemStatus()
    systemStatus.cleanup()
    print("Please spin all the flaps to show the letter A")
    for i in range (1, self._config.get(Keywords.NUMBER_OF_MOTORS) + 1):
      print("Now configuring the character " + str(i))
      # This will help us take the ticks variable to zero (first appearance of the letter = 0)
      # Plus it will also configure our sequence to execute correctly (if the motor is waiting for 
      # sequence 5 and we start from zero, it will ignore our calls 0-4, and start turning from 5 onwards.
      while not Utils.askForConfirmation("Is it showing letter B now?"):
        controller.tick()
      systemStatus.set(i, 0, self._config.get(Keywords.CHARACTERS_ARRAY).index('B'), controller.getSequence().currentIndex())
    systemStatus.save()
    print("Great, now the split-flap is correctly configured")
      
class CalibratorCharacter:

  def __init__(self, pinBuilder):
    factory = DisplayFactory(pinBuilder, defaultSystemConfiguration(), cleanSystemStatus())
    self._sequence, self._connection = factory.buildCharacterCalibrator()
    
  def getSequence(self):
    return self._sequence
    
  def tick(self):
    self._sequence.next()
    self._connection.publish()
