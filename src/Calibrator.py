from Configuration import defaultSystemConfiguration, cleanSystemStatus
from DisplayFactory import DisplayFactory
from Configuration import Keywords
from Logger import log
import Utils
import time

# This class takes care of the calibration of each character. Calibration consists on figuring out how many steps of the sequence 
# are needed to change a letter, and also on setting the initial positions for each letter.
class Calibrator:
  def __init__(self, pinBuilder):
    self._pinBuilder = pinBuilder
    self._config = defaultSystemConfiguration()

  def infiniteRun(self):
    controller = _CalibratorCharacter(self._pinBuilder, 1)
    while True:
      controller.tick()
      time.sleep(0.001)
        
  def calibrateTicksPerLetter(self):
      self.divideAndConquerTicksPerLetter()
    
  def divideAndConquerTicksPerLetter(self):
    controller = _CalibratorCharacter(self._pinBuilder, 1)
    print("Please take a look at the first character, we will need to validate when the letter is changed for setup")
    
    ticks = self.divideAndConquer(controller, 50, 100)
    
    self._config.setTicksPerLetter(ticks)
    self._config.save()

  # If value is 76, (50, 100) -> (75, 100) -> (75, 87) -> ....
  def divideAndConquer(self, controller, lowValue, highValue):
    if lowValue == highValue:
        return lowValue
    
    log(Calibrator.__name__, "Calibrator", "Testing range (" + str(lowValue) + ", " + str(highValue) + ")")
    for _ in range(highValue * 2):
      controller.tick(0)
    highValueTurnedLetter = Utils.askForConfirmation("Did it change two letters?")
    for _ in range(lowValue * 2):
      controller.tick(0)
    lowValueTurnedLetter = Utils.askForConfirmation("Did it change two letters?")
    
    # To avoid getting stuck in loops due to int casting
    if highValue - lowValue == 1:
      if highValueTurnedLetter and lowValueTurnedLetter:
        return lowValue
      elif highValueTurnedLetter and not lowValueTurnedLetter:
        return highValue
    
    if highValueTurnedLetter and lowValueTurnedLetter:
      return self.divideAndConquer(controller, int(lowValue/2), lowValue)
    elif highValueTurnedLetter and not lowValueTurnedLetter:
      return self.divideAndConquer(controller, int(lowValue + ((highValue - lowValue)/2)), highValue)
    elif not highValueTurnedLetter and not lowValueTurnedLetter:
      return self.divideAndConquer(controller, int(lowValue/2), lowValue)
    else:
      raise Exception("Low value " + str(lowValue) + "turned letter, but high one " + str(highValue) + " didn't")
        
  def calibrateInitialPosition(self):
    numberOfMotors = self._config.get(Keywords.NUMBER_OF_MOTORS)
    controller = _CalibratorCharacter(self._pinBuilder, numberOfMotors)
    systemStatus = cleanSystemStatus()
    systemStatus.cleanup()
    for i in range (1, numberOfMotors + 1):
      print("Now configuring the character " + str(i))
      # This will help us take the ticks variable to zero (first appearance of the letter = 0)
      # Plus it will also configure our sequence to execute correctly (if the motor is waiting for 
      # sequence 5 and we start from zero, it will ignore our calls 0-4, and start turning from 5 onwards.
      while not Utils.askForConfirmation("Is it showing letter B now?", True):
        controller.tick(i-1)
      systemStatus.set(i, 0, self._config.get(Keywords.CHARACTERS_ARRAY).index('B'), controller.getSequence().currentIndex())
    systemStatus.save()
    print("Great, now the split-flap is correctly configured")
  
class _CalibratorCharacter:
  def __init__(self, pinBuilder, quantity):
    factory = DisplayFactory(pinBuilder, defaultSystemConfiguration(), cleanSystemStatus())
    self._sequences, self._connection = factory.buildCharacterCalibrator(quantity)
    
  def getSequences(self):
    return self._sequences
    
  def tick(self, index):
    self._sequences[index].next()
    self._connection.publish()
