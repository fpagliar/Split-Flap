from MotorSequence import MotorSequence
from Display import Display
from Character import Character, CharacterSequence
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
    # TODO: get the correct values to create the sequence
#     for motorId in range(numberOfMotors):
#       characterSequence = CharacterSequence(motorId + 1, possibleValues, indexChanges, currentIndex)
#     characters = [Character(motorId + 1, sequences[motorId], characterSequence) for motorId in range(numberOfMotors)]
    characters = []
    for motorId in range(numberOfMotors):
      characterSequence = _UndefinedLengthSequence(self._config.alphabet())
      characters.append(Character(motorId + 1, sequences[motorId], characterSequence))
    for character in characters:
      character.registerListener(systemStatus)
    return characters, SequencePublisher(sequences, connection)

#   def standardCharacterSequence(self, motorId):
#     return CharacterSequence(motorId, self._config.alphabet(), self._cali, currentIndex)

class _UndefinedLengthSequence:
  def __init__(self, values):
    self._values = values
    self._ticks = 0

  def next(self):
    self._ticks = self._ticks + 1

  def isMatching(self, value):
    return False

  def __contains__(self, key):
    return key in self._values

  def inform(self, listener):
    listener(self._ticks)

