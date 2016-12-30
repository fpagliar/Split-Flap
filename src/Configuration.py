import os.path

def serializeCollection(name, iterable):
  return serializeValue(name, "|".join([str(elem) for elem in iterable]))

def serializeValue(name, value):
  return name + ": " + str(value) + "\n"

def loadCollection(line, name, func = False):
  prefix = name + ": "
  if prefix in line:
    line = line[len(prefix):]
  tokens = line.split("|")
  if func:
    tokens = [func(elem) for elem in tokens]
  return tokens

def loadValue(line, name, func = False):
  prefix = name + ": "
  if prefix in line:
    line = line[len(prefix):]
  if func:
    line = func(line) 
  return line

def defaultConfiguration():
  config = Configuration("properties.config")
  config.setDefaults()
  return config

class Configuration:
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
    self.CHARACTERS_ARRAY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', ' ', ' ', ' ']
    self.MULTIPLEXER_PINS = [1, 2, 3, 4]
    self.SEQUENCE_PINS = [5, 6, 7, 8]
    self.TICKS_PER_LETTER = 3
    self.MULTIPLEXER_POWER_PIN = 10
    self.NUMBER_OF_MOTORS = 10
    self.FEED_FILENAME = "feed.txt"
    self.LOG_FILENAME = "log.txt"
    
  def save(self):
    with open(self._filename, "w+") as file:    
      file.truncate(0)
      file.write(serializeCollection("CHARACTERS_ARRAY" , self.CHARACTERS_ARRAY))
      file.write(serializeCollection("MULTIPLEXER_PINS", self.MULTIPLEXER_PINS))
      file.write(serializeCollection("SEQUENCE_PINS", self.SEQUENCE_PINS))
      file.write(serializeValue("TICKS_PER_LETTER", self.TICKS_PER_LETTER))
      file.write(serializeValue("MULTIPLEXER_POWER_PIN", self.MULTIPLEXER_POWER_PIN))
      file.write(serializeValue("NUMBER_OF_MOTORS", self.NUMBER_OF_MOTORS))
      file.write(serializeValue("FEED_FILENAME", self.FEED_FILENAME))
      file.write(serializeValue("LOG_FILENAME", self.LOG_FILENAME))
        
  def load(self):
    if os.path.isfile(self._filename):
      with open(self._filename, "r+") as file:
        lines = [line.rstrip('\n') for line in file]
        self.CHARACTERS_ARRAY      = loadCollection(lines[0], 'CHARACTERS_ARRAY')
        self.MULTIPLEXER_PINS      = loadCollection(lines[1], 'MULTIPLEXER_PINS', int)
        self.SEQUENCE_PINS         = loadCollection(lines[2], 'SEQUENCE_PINS', int)
        self.TICKS_PER_LETTER      = loadValue(lines[3], 'TICKS_PER_LETTER', int)
        self.MULTIPLEXER_POWER_PIN = loadValue(lines[4], 'MULTIPLEXER_POWER_PIN', int)
        self.NUMBER_OF_MOTORS      = loadValue(lines[5], 'NUMBER_OF_MOTORS', int)
        self.FEED_FILENAME         = loadValue(lines[6], 'FEED_FILENAME')
        self.LOG_FILENAME          = loadValue(lines[7], 'LOG_FILENAME')    