from MotorSequence import MotorSequence
from Display import Display
from Configuration import Keywords
from Character import Character
from Timer import Timer
from ShiftRegistry import buildShiftRegistry

class DisplayFactory:
  def __init__(self, pinBuilder, configuration, systemStatus):
    self._pinBuilder = pinBuilder
    self._config = configuration
    self._systemStatus = systemStatus
    
  def _getPin(self, keyword):
    return self._pinBuilder(self._config.get(keyword))
  
  def build(self):
    numberOfMotors = self._config.get(Keywords.NUMBER_OF_MOTORS)

    dataPin = self._getPin(Keywords.DATA_PIN)
    clockPin = self._getPin(Keywords.CLOCK_PIN)
    shiftPin = self._getPin(Keywords.SHIFT_PIN)
    
    sequences = [self._createMotorSequence(i + 1) for i in range(numberOfMotors)]

    shiftRegistry = buildShiftRegistry(dataPin, clockPin, shiftPin, Timer(), sequences)
    characters = [Character(motorId + 1, sequences[motorId], self._config, self._systemStatus) for motorId in range(numberOfMotors)]
    return Display(characters, shiftRegistry)    
  
  def _createMotorSequence(self, motorId):
    return MotorSequence(self._config.MOTOR_SEQUENCE, self._systemStatus.getSequenceIndex(motorId))
  
  def _createPinsFromIds(self, ids):
    return [self._pinBuilder(ids[i]) for i in range(len(ids))]
