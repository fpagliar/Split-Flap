
def CreateCharacter(pinId, controller, properties):
  return Character(pinId, controller, properties)

class Character:
  def __init__(self, pinId, controller, properties):
        self._pinId = pinId
        self._controller = controller
        self._properties = properties
        self._currentLetterIndex = 0
        self._targetLetterIndex = 0
        self._currentTicks = 0
          
  def tick(self):
    if self._currentLetterIndex != self._targetLetterIndex:
      # Increment the number of ticks in this letter
      self._currentTicks = self._currentTicks + 1
      # Make the controller send a tick to the motor 
      self._controller.tick(self._pinId)
      if self._currentTicks == self._properties.TICKS_PER_LETTER:
        self._currentTicks = 0
        self._setNextLetter()
    else:
      print("Target letter reached")
  
  def setTarget(self, letter):
    self._targetLetterIndex = self._properties.CHARACTERS_ARRAY.index(letter)
    print("Setting target: " + str(self._targetLetterIndex) + " -> " + self.getTargetLetter())
  
  def isReady(self):
    return self._currentLetterIndex == self._targetLetterIndex
  
  def getCurrentLetter(self):
    return self._properties.CHARACTERS_ARRAY[self._currentLetterIndex]

  def getTargetLetter(self):
    return self._properties.CHARACTERS_ARRAY[self._targetLetterIndex]

  def _setNextLetter(self):
    pos = self._currentLetterIndex
    pos = pos + 1
    if pos == len(self._properties.CHARACTERS_ARRAY):
      pos = 0
    self._currentLetterIndex = pos
    print("\n\nCurrent letter " + self.getCurrentLetter())
