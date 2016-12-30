
def CreateCharacter(pinId, controller, configuration):
  return Character(pinId, controller, configuration)

class Character:
  def __init__(self, motorId, controller, configuration, systemStatus):
        self._motorId = motorId
        self._controller = controller
        self._configuration = configuration
        self._systemStatus = systemStatus
        self._currentLetterIndex = self._systemStatus.getCurrentLetterIndex(motorId)
        self._targetLetterIndex = 0
        self._currentTicks = self._systemStatus.getCurrentTicks(motorId)
  
  def tick(self):
    if self._currentLetterIndex != self._targetLetterIndex:
      # Increment the number of ticks in this letter
      self._currentTicks = self._currentTicks + 1
      if self._currentTicks == self._configuration.TICKS_PER_LETTER:
        self._currentTicks = 0
        self._setNextLetter()
      
      # Update the current system status
      self._systemStatus.set(self._motorId, self._currentTicks, self._currentLetterIndex)
      # Cleanup the old status before executing the change
      self._systemStatus.cleanup()
      # Make the controller send a tick to the motor
      self._controller.tick(self._motorId)
      # Write the new system status. If there is a failure/program is killed between the cleanup and 
      # the save, we lose the status, but that is OK since it wouldn't be possible to figure out if the call
      # was executed successfully or not.
      self._systemStatus.save()
  
  def setTarget(self, letter):
    self._targetLetterIndex = self._configuration.CHARACTERS_ARRAY.index(letter)
  
  def isReady(self):
    return self._currentLetterIndex == self._targetLetterIndex
  
  def getCurrentLetter(self):
    return self._configuration.CHARACTERS_ARRAY[self._currentLetterIndex]

  def getTargetLetter(self):
    return self._configuration.CHARACTERS_ARRAY[self._targetLetterIndex]

  def _setNextLetter(self):
    pos = self._currentLetterIndex
    pos = pos + 1
    if pos == len(self._configuration.CHARACTERS_ARRAY):
      pos = 0
    self._currentLetterIndex = pos
