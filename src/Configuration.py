import collections
import os.path
from enum import Enum

class ConfigurationFile:
  _keySeparator = ":"
  _collectionSeparator = "|"

  def __init__(self, fileName):
    self._fileName = fileName
    self._mappings = {}

  def get(self, keyword):
    return self._mappings[keyword]

  def set(self, keyword, value):
    self._mappings[keyword] = value

  def cleanup(self):
    with open(self._filename, "w+") as file:
      file.truncate(0)

  def save(self):
    with open(self._filename, "w+") as file:
      file.truncate(0)
      for key in self._mappings:
        file.write(self._serialize(key, self._mappings[key]))

  def _serializeValue(self, key, value):
    return str(key) + ConfigurationFile._keySeparator + str(value) + "\n"

  def _serialize(self, key, value):
    if isinstance(value, collections.Iterable):
      value = ConfigurationFile._collectionSeparator.join([str(elem) for elem in value])
    return self._serializeValue(key, value)

  def load(self, loaderMap):
    if os.path.isfile(self._fileName):
      with open(self._fileName, "r+") as file:
        for line in file:
          self._loadLine(line, loaderMap)

  def _loadLine(self, line, loaderMap):
    strippedLine = line.strip()
    keySeparator = ConfigurationFile._keySeparator
    collectionSeparator = ConfigurationFile._collectionSeparator
    if keySeparator in strippedLine:
      key = strippedLine.split(keySeparator)[0]
      if key not in loaderMap:
        raise Exception("Invalid key found in file: " + str(key))
      value = (strippedLine[len(key) + 1:])
      if collectionSeparator in value:
        tokens = value.split(collectionSeparator)
        self._mappings[key] = [loaderMap[key](elem) for elem in tokens]
      else:
        self._mappings[key] = loaderMap[key](value)

class _SystemKeywords(Enum):
    NUMBER_OF_MOTORS = "NUMBER_OF_MOTORS"
    USE_DIRECT_CONNECTION = "USE_DIRECT_CONNECTION"
    SEQUENCE_PINS = "SEQUENCE_PINS"
    DATA_PIN = "DATA_PIN"
    CLOCK_PIN = "CLOCK_PIN"
    SHIFT_PIN = "SHIFT_PIN"
    DEBUG_MODE = "DEBUG_MODE"
    USE_TEXT_PINS = "USE_TEXT_PINS"
    LOGGER_TAGS = "LOGGER_TAGS"
    ALPHABET = "ALPHABET"

    def __str__(self):
        return str(self.value)

def str2bool(v):
  return v.strip().lower() in ("yes", "true", "t", "1")

class SystemConfiguration:
  _fileName = "system.config"

  def __init__(self):
    self._config = ConfigurationFile(SystemConfiguration._fileName)
    self._load()
    self.MOTOR_SEQUENCE = [
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
      ][::-1]

  def _load(self):
    loaderMap = {
      _SystemKeywords.NUMBER_OF_MOTORS : int,
      _SystemKeywords.DATA_PIN : int,
      _SystemKeywords.CLOCK_PIN : int,
      _SystemKeywords.SHIFT_PIN : int,
      _SystemKeywords.SEQUENCE_PINS: int,
      _SystemKeywords.DEBUG_MODE: str2bool,
      _SystemKeywords.USE_TEXT_PINS: str2bool,
      _SystemKeywords.USE_DIRECT_CONNECTION: str2bool,
      _SystemKeywords.LOGGER_TAGS: str,
      _SystemKeywords.ALPHABET: str,
    }

    loaderMap = dict((str(key), val) for key, val in loaderMap.items())
    self._config.load(loaderMap)

  def save(self):
    self._config.save()

  def _get(self, keyword):
    return self._config.get(str(keyword))

  def numberOfMotors(self):
    return self._get(_SystemKeywords.NUMBER_OF_MOTORS)

  def motorSequence(self):
    return self.MOTOR_SEQUENCE

  def useDirectConnection(self):
    return self._get(_SystemKeywords.USE_DIRECT_CONNECTION)

  def sequencePins(self):
    if self.useDirectConnection():
      return self._get(_SystemKeywords.SEQUENCE_PINS)
    else:
      raise Exception("Use direct connection is set to False, you should be using a shift registry")

  def shiftRegistryPins(self):
    if self.useDirectConnection():
      raise Exception("Use direct connection is set to True, so you should be using the sequence pins")
    else:
      return (self._get(_SystemKeywords.DATA_PIN), self._get(_SystemKeywords.CLOCK_PIN), self._get(_SystemKeywords.SHIFT_PIN))

  def isDebugMode(self):
    return self._get(_SystemKeywords.DEBUG_MODE)

  def shouldUseTextPins(self):
    if self.isDebugMode():
      return self._get(_SystemKeywords.USE_TEXT_PINS)
    else:
      return False

  def shouldLog(self, tag):
    if self.isDebugMode():
      return tag in self._get(_SystemKeywords.LOGGER_TAGS)
    else:
      return []

  def alphabet(self):
    return self._get(_SystemKeywords.ALPHABET)

class MotorConfigurationFile:
  _separator = ">"

  def __init__(self, fileName, numberOfMotors):
    self._config = ConfigurationFile(fileName)
    self._numberOfMotors = numberOfMotors

  def _getKey(self, motorId, field):
    return str(motorId) + MotorConfigurationFile._separator + field

  def save(self):
    self._config.save()

  def cleanup(self):
    self._config.cleanup()

  def load(self, keyFunctionMap):
    loaderMap = { }
    for i in range(1, self._numberOfMotors + 1):
      for key in keyFunctionMap:
        loaderMap[self._getKey(i, key)] = keyFunctionMap[key]
    self._config.load(loaderMap)

  def get(self, motorId, key):
    return self._config.get(self._getKey(motorId, key))

  def set(self, motorId, key, value):
    if motorId not in range(1, self._numberOfMotors + 1):
      raise Exception("Invalid motor id: " + str(motorId))
    self._config.set(self._getKey(motorId, key), value)

class SystemStatus:
  _fileName = "system.status"
  _ticksKey = "TICKS"
  _sequenceKey = "SEQUENCE_INDEX"

  def __init__(self, numberOfMotors):
    self._config = MotorConfigurationFile(SystemStatus._fileName, numberOfMotors)

  def set(self, motorId, currentTicks, sequenceIndex):
    self._config.set(SystemStatus._ticksKey, currentTicks)
    self._config.set(SystemStatus._sequenceKey, sequenceIndex)

  def ticks(self, motorId):
    return self._config.get(motorId, SystemStatus._ticksKey)

  def sequence(self, motorId):
    return self._config.get(motorId, SystemStatus._sequenceKey)

  def save(self):
    self._config.save()

  def cleanup(self):
    self._config.cleanup()

  def load(self):
    self._config.load({ SystemStatus._sequenceKey: int, SystemStatus._ticksKey: int})

class SystemCalibration:
  _fileName = "system.calibration"
  _key = "LETTER_CHANGES"

  def __init__(self, numberOfMotors):
    self._config = MotorConfigurationFile(SystemStatus._fileName, numberOfMotors)

  def set(self, motorId, ticksConfiguration):
    self._config.set(SystemCalibration._key, ticksConfiguration)

  def ticksConfiguration(self, motorId):
    return self._config.get(motorId, SystemCalibration._key)

  def save(self):
    self._config.save()

  def cleanup(self):
    self._config.cleanup()

  def load(self):
    self._config.load({ SystemCalibration._key : int})
