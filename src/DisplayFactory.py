from MotorSequence import MotorSequence
from Display import Display
from Configuration import Keywords
from Character import Character
from Timer import Timer
from Connection import buildConnection, SequencePublisher
from Logger import log

# This class is a factory to produce the different types of displays based on the configuration provided.
class DisplayFactory:
  def __init__(self, pinBuilder, configuration, systemStatus):
    self._pinBuilder = pinBuilder
    self._config = configuration
    self._systemStatus = systemStatus
    
  def buildCharacterCalibrator(self, quantity):
    sequences = [self._createMotorSequence(i + 1) for i in range(quantity)]
    connection = buildConnection(self._config, self._pinBuilder, quantity, Timer())
    publisher = SequencePublisher(sequences, connection)
    return sequences, publisher

  def buildCharacterTester(self):
    sequence, connection = self.buildCharacterCalibrator()
    publisher = SequencePublisher([sequence], connection)
    character = Character(1, sequence, self._config, self._systemStatus)
    return Display([character], publisher)
    
  def _getPin(self, keyword):
    return self._pinBuilder(self._config.get(keyword))
  
  def build(self):
    numberOfMotors = self._config.get(Keywords.NUMBER_OF_MOTORS)
    sequences = [self._createMotorSequence(i + 1) for i in range(numberOfMotors)]
    connection = buildConnection(self._config, self._pinBuilder, numberOfMotors, Timer())
    characters = [Character(motorId + 1, sequences[motorId], self._config, self._systemStatus) for motorId in range(numberOfMotors)]
    return Display(characters, SequencePublisher(sequences, connection))
  
  def _createMotorSequence(self, motorId):
    return MotorSequence(self._config.MOTOR_SEQUENCE, self._systemStatus.getSequenceIndex(motorId))
  
  def _createPinsFromIds(self, ids):
    return [self._pinBuilder(ids[i]) for i in range(len(ids))]
