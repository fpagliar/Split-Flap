from Configuration import Keywords
from Logger import log

class Character:
  def __init__(self, motorId, sequence, configuration, systemStatus):
    log("Creating character with id: " + str(motorId))
    self._motorId = motorId
    self._sequence = sequence
    self._configuration = configuration
    self._systemStatus = systemStatus
    self._currentLetterIndex = self._systemStatus.getCurrentLetterIndex(motorId)
    self._targetLetterIndex = 0
    self._currentTicks = self._systemStatus.getCurrentTicks(motorId)
  
  def tick(self):
    if not self.hasFinished():
      # Increment the number of ticks in this letter
      self._increment()
      # Cleanup the old status before executing the change
      self._systemStatus.cleanup()
      # Move the motor sequence
      self._sequence.next()
      # Update the current system status
      self._systemStatus.set(self._motorId, self._currentTicks, self._currentLetterIndex, 
                             self._sequence.currentIndex())
      # Write the new system status. If there is a failure/program is killed between the cleanup and 
      # the save, we lose the status, but that is OK since it wouldn't be possible to figure out if the call
      # was executed successfully or not.
      self._systemStatus.save()
  
  def _increment(self):
    self._currentTicks += 1
    if self._currentTicks == self._configuration.get(Keywords.TICKS_PER_LETTER):
      self._currentTicks = 0
      self._setNextLetter()
    log("Incrementing ticks for character(" + str(self._motorId) + ") to: " + str(self._currentTicks))
  
  def hasFinished(self):
    return self._currentLetterIndex == self._targetLetterIndex
  
  def setTarget(self, letter):
    log("Setting target for character(" + str(self._motorId) + "): " + letter)
    self._targetLetterIndex = self._configuration.get(Keywords.CHARACTERS_ARRAY).index(letter)
  
  def isReady(self):
    return self._currentLetterIndex == self._targetLetterIndex
  
  def getCurrentLetter(self):
    return self._configuration.get(Keywords.CHARACTERS_ARRAY)[self._currentLetterIndex]

  def getTargetLetter(self):
    return self._configuration.get(Keywords.CHARACTERS_ARRAY)[self._targetLetterIndex]
  
  def getCurrentStatus(self):
    return (self.getCurrentLetter(), self._currentTicks, self._sequence)

  def _setNextLetter(self):
    pos = self._currentLetterIndex
    pos = pos + 1
    if pos == len(self._configuration.get(Keywords.CHARACTERS_ARRAY)):
      pos = 0
    self._currentLetterIndex = pos
    log("Setting letter for character(" + str(self._motorId) + "): " + self.getCurrentLetter())
