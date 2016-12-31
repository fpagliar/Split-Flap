from MotorController import MotorController
from MotorCommunicator import MotorCommunicator
from Multiplexor import Multiplexor
from MotorSequence import MotorSequence
from Display import Display
from Character import Character

class DisplayFactory:
  def __init__(self, pinBuilder, configuration, systemStatus):
    self._pinBuilder = pinBuilder
    self._config = configuration
    self._systemStatus = systemStatus
    
  def build(self):
    multiplexorPins = self._createPinsFromIds(self._config.MULTIPLEXER_PINS)
    powerPin = self._pinBuilder(self._config.MULTIPLEXER_POWER_PIN)
    multiplexor = Multiplexor(multiplexorPins, powerPin)
    sequences = [self._createMotorSequence(i+1) for i in range(self._config.NUMBER_OF_MOTORS)]
    controller = MotorController(MotorCommunicator(multiplexor), sequences)
    return Display([Character(motorId, controller, self._config, self._systemStatus) for motorId in range(1, self._config.NUMBER_OF_MOTORS + 1)])
  
  def _createMotorSequence(self, motorId):
    return MotorSequence(self._createPinsFromIds(self._config.SEQUENCE_PINS), self._config.MOTOR_SEQUENCE, 
                         self._systemStatus.getSequenceIndex(motorId))
  
  def _createPinsFromIds(self, ids):
    return [self._pinBuilder(ids[i]) for i in range(len(ids))]