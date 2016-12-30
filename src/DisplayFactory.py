from MotorController import MotorController
from MotorCommunicator import MotorCommunicator
from Multiplexor import Multiplexor
from Configuration import defaultSystemConfiguration, defaultSystemStatus
from MotorSequence import MotorSequence
from Display import Display
from Character import Character

class DisplayFactory:
  def __init__(self, pinBuilder):
    self._pinBuilder = pinBuilder
    self._config = defaultSystemConfiguration()
    
  def build(self):
    systemStatus = defaultSystemStatus()
    multiplexorPins = self._createPinsFromIds(self._config.MULTIPLEXER_PINS)
    powerPin = self._pinBuilder(self._config.MULTIPLEXER_POWER_PIN)
    multiplexor = Multiplexor(multiplexorPins, powerPin)
    controller = MotorController(self._config.NUMBER_OF_MOTORS, MotorCommunicator(multiplexor), self._sequenceBuilder)    
    return Display([Character(motorId, controller, self._config, systemStatus) for motorId in range(1, self._config.NUMBER_OF_MOTORS + 1)])
  
  def _createPinsFromIds(self, ids):
    return [self._pinBuilder(ids[i]) for i in range(len(ids))]    
  
  def _sequenceBuilder(self):
    return MotorSequence(self._createPinsFromIds(self._config.SEQUENCE_PINS), self._config.MOTOR_SEQUENCE)
