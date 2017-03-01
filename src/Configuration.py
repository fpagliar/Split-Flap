import os.path
from enum import Enum

def serializeCollection(name, iterable):
  return serializeValue(name, "|".join([str(elem) for elem in iterable]))

def serializeValue(name, value):
  return name + ": " + str(value) + "\n"

def loadCollection(line, name, func=False):
  prefix = name + ": "
  if prefix in line:
    line = line[len(prefix):]
  tokens = line.split("|")
  if func:
    tokens = [func(elem) for elem in tokens]
  return tokens

def loadValue(line, name, func=False):
  prefix = name + ": "
  if prefix in line:
    line = line[len(prefix):]
  if func:
    line = func(line) 
  return line

def defaultSystemConfiguration():
  config = SystemConfiguration("properties.config")
  config.setDefaults()
  config.load()
  return config

def defaultSystemStatus():
  status = SystemStatus("system_status.config")
  status.load()
  return status

def cleanSystemStatus():
  return SystemStatus("system_status.config")

class Keywords(Enum):
    TICKS_PER_LETTER = "TICKS_PER_LETTER"
    NUMBER_OF_MOTORS = "NUMBER_OF_MOTORS"
    FEED_FILENAME = "FEED_FILENAME"
    LOG_FILENAME = "LOG_FILENAME"
    CHARACTERS_ARRAY = "CHARACTERS_ARRAY"
    DATA_PIN = "DATA_PIN"
    CLOCK_PIN = "CLOCK_PIN"
    SHIFT_PIN = "SHIFT_PIN"
    SEQUENCE_PINS = "SEQUENCE_PINS"

class SystemConfiguration:
  def __init__(self, filename):
    self.MOTOR_SEQUENCE = [
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
      ]
    self._filename = filename
    
  def setDefaults(self):
    self.values = {
      Keywords.TICKS_PER_LETTER : 3,
      Keywords.NUMBER_OF_MOTORS : 10,
      Keywords.FEED_FILENAME : "feed.txt",
      Keywords.LOG_FILENAME : "log.txt",
      Keywords.DATA_PIN : 10,
      Keywords.CLOCK_PIN : 11,
      Keywords.SHIFT_PIN : 12,
    }

    self.collections = {
        Keywords.CHARACTERS_ARRAY : ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', ' ', ' ', ' '],
        Keywords.SEQUENCE_PINS : [10, 11, 12, 13]
    }
  
  def get(self, key):
    if key in self.values:
      return self.values[key]
    else:
      return self.collections[key]  
  
  def save(self):
    with open(self._filename, "w+") as file:    
      file.truncate(0)
      for key in self.values:
        file.write(serializeValue(key, self.values[key]))
      for key in self.collections:
        file.write(serializeCollection(key, self.collections[key]))
        
  def load(self):
    if os.path.isfile(self._filename):
      with open(self._filename, "r+") as file:
        lines = [line.rstrip('\n') for line in file]
        i = 0
        for key in self.values:
          self.values[key] = loadValue(lines[i], key, int)
          i = i + 1
        for key in self.collections:
          self.collections[key] = loadCollection(lines[i], key)
          i = i + 1

class SystemStatus:
  def __init__(self, filename):
    self._filename = filename
    self._details = {}
    self._ticksKey = "TICKS"
    self._indexKey = "LETTER_INDEX"
    self._sequenceKey = "SEQUENCE_INDEX"
    self._keySeparator = ">"
  
  def set(self, motorId, currentTicks, currentLetterIndex, sequenceIndex):
    self._details[motorId] = { self._ticksKey: currentTicks, self._indexKey: currentLetterIndex, self._sequenceKey: sequenceIndex }
  
  def save(self):
    with open(self._filename, "w+") as file:
      for key, value in self._details.items():
        file.write(serializeValue(str(key) + self._keySeparator + self._ticksKey , value[self._ticksKey]))
        file.write(serializeValue(str(key) + self._keySeparator + self._indexKey , value[self._indexKey]))
        file.write(serializeValue(str(key) + self._keySeparator + self._sequenceKey , value[self._sequenceKey]))
  
  def cleanup(self):
    with open(self._filename, "w+") as file:
      file.truncate(0)
      
  def load(self):
    with open(self._filename, "r+") as file:
      for line in file:
        motorId, rest = line.split(self._keySeparator)
        motorId = int(motorId)
        key, value = rest.split(":")
        if motorId not in self._details:
          self._details[motorId] = {}
        self._details[motorId][key] = int(value)
  
  def getCurrentTicks(self, motorId):
    return self._getDetail(motorId, self._ticksKey)

  def getCurrentLetterIndex(self, motorId):
    return self._getDetail(motorId, self._indexKey)

  def getSequenceIndex(self, motorId):
    return self._getDetail(motorId, self._sequenceKey)

  def _getDetail(self, motorId, key):
    if motorId in self._details and key in self._details[motorId]:
      return self._details[motorId][key]
    else:
      return 0
