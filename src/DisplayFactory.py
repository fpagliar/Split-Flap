from MotorSequence import MotorSequence
from Display import Display
from Character import Character
from Timer import Timer
from Connection import buildConnection, SequencePublisher, _ShiftRegistry, _ShiftRegistryController
from Logger import log

# This class is a factory to produce the different types of displays based on the configuration provided.
class DisplayFactory:
  def __init__(self, pinBuilder, configuration):
    self._pinBuilder = pinBuilder
    self._config = configuration

  def _getPin(self, keyword):
    return self._pinBuilder(self._config.get(keyword))

  def _createPinsFromIds(self, ids):
    return [self._pinBuilder(ids[i]) for i in range(len(ids))]

  def _createMotorSequence(self, motorId, sequenceIndex):
    return MotorSequence(motorId, self._config.MOTOR_SEQUENCE, sequenceIndex)

  def buildCharacterCalibrator(self, quantity):
    sequences = [self._createMotorSequence(i + 1, 0) for i in range(quantity)]
    connection = buildConnection(self._config, self._pinBuilder, quantity, Timer())
    publisher = SequencePublisher(sequences, connection)
    return sequences, publisher

  def buildShiftRegistry(self, length):
    data, clock, shift = self._config.shiftRegistryPins()
    controller = _ShiftRegistryController(self._pinBuilder(data), self._pinBuilder(clock), self._pinBuilder(shift), Timer())
    return _ShiftRegistry(controller, length)

  def buildDisplay(self, systemStatus):
    characters, publisher = self.buildCharacters(systemStatus)
    return Display(characters, publisher)

  def buildCharacters(self, systemStatus):
    numberOfMotors = self._config.numberOfMotors()
    sequences = [self._createMotorSequence(i + 1, systemStatus.sequence(i + 1)) for i in range(numberOfMotors)]
    connection = buildConnection(self._config, self._pinBuilder, numberOfMotors, Timer())
    characters = [Character(motorId + 1, sequences[motorId], self._config) for motorId in range(numberOfMotors)]
    for character in characters:
      character.registerListener(systemStatus)
    return characters, SequencePublisher(sequences, connection)

