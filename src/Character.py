from Configuration import Keywords
from Logger import log

# This class receives a motor sequence, and tracks the logical characters that should be being shown
# as that sequence progresses. So it basically keeps a mapping between a character, and its corresponding motor state.
# 
# It also persists the current system status after each change, in order to be able to save the state if the program is shut down.
# Usage: 
#       - setTarget:  Sets the letter that we want to show (and is potentially different from what we are showing at the moment).
#                     ex: the display is currently showing C, but we want to show A, so we invoke setTarget('A')
#       - tick:       Marks that a unit of time has passed, and so if the target is not met yet, we should move a unit towards it.
#                     In order to move for it, we should increment the sequence on the motor, and make update the logic on the character to match it.

class Character:
  def __init__(self, motorId, sequence, configuration, systemStatus):
    log(Character.__name__, "Character - " + str(motorId), "Creating character with id: " + str(motorId))
    self._motorId = motorId
    self._sequence = sequence
    self._configuration = configuration
    self._systemStatus = systemStatus
    self._currentLetterIndex = self._systemStatus.getCurrentLetterIndex(motorId)
    self._targetLetterIndex = 0
    self._currentTicks = self._systemStatus.getCurrentTicks(motorId)
  
  def tick(self):
    log(Character.__name__, "Character - " + str(self._motorId), "Tick")
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
    log(Character.__name__, "Character - " + str(self._motorId), "Incrementing ticks to: " + str(self._currentTicks))
  
  def hasFinished(self):
    return self._currentLetterIndex == self._targetLetterIndex
  
  def setTarget(self, letter):
    log(Character.__name__, "Character - " + str(self._motorId), "Setting target: " + letter)
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
    log(Character.__name__, "Character - " + str(self._motorId), "Setting letter: " + self.getCurrentLetter())
