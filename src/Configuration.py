
def serializeCollection(self, name, iterable):
  return name + ": " + "|".join(iterable)

def serializeValue(self, name, value):
  return name + ": " + str(value)

def loadCollection(self, line, name, func = False):
  prefix = name + ": "
  if prefix in line:
    line = line[len(prefix):]
  tokens = line.split("|")
  if func:
    tokens = [func(elem) for elem in tokens]
  return tokens

def loadValue(self, line, name, func = False):
  prefix = name + ": "
  if prefix in line:
    line = line[len(prefix):]
  if func:
    line = func(line) 
  return line

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
    
  def save(self):
    with open(self._filename, "w+") as file:    
      file.truncate(0)
      file.write(serializeCollection("CHARACTERS_ARRAY" , self.CHARACTERS_ARRAY))
      file.write(serializeCollection("MULTIPLEXER_PINS", self.MULTIPLEXER_PINS))
      file.write(serializeCollection("SEQUENCE_PINS", self.SEQUENCE_PINS))
      file.write(serializeValue("TICKS_PER_LETTER", self.TICKS_PER_LETTER))
      file.write(serializeValue("FEED_FILENAME", self.FEED_FILENAME))
      file.write(serializeValue("LOG_FILENAME", self.LOG_FILENAME))
        
  def load(self):
    with open(self._filename, "r+") as file:
      lines = [line.rstrip('\n') for line in file]
      self.CHARACTERS_ARRAY = loadCollection(lines[0], 'CHARACTERS_ARRAY')
      self.MULTIPLEXER_PINS = loadCollection(lines[1], 'MULTIPLEXER_PINS', int)
      self.SEQUENCE_PINS = loadCollection(lines[2], 'SEQUENCE_PINS', int)
      self.TICKS_PER_LETTER = loadValue(lines[3], 'TICKS_PER_LETTER', int)
      self.FEED_FILENAME = loadValue(lines[4], 'FEED_FILENAME')
      self.LOG_FILENAME = loadValue(lines[5], 'LOG_FILENAME')    
#     self.CHARACTERS_ARRAY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', ' ', ' ', ' ']
