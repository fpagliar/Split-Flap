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
  def __init__(self, motorId, motorSequence, characterSequence):
    log(self, "Creating character with id: " + str(motorId))
    self._motorId = motorId
    self._motorSequence = motorSequence
    self._characterSequence = characterSequence
    self._targetLetter = 'A'
    self._listeners = []

  def registerListener(self, statusListener):
    self._listeners.append(statusListener)

  def _publishStatus(self):
    self._informListeners(lambda l : self._motorSequence.inform(
      _Reporter(self._motorId, self._characterSequence, l).forMotorSequenceIndex))

  def _clearStatus(self):
    self._informListeners(lambda x : x.cleanup())

  def _informListeners(self, informingFunction):
    for listener in self._listeners:
      informingFunction(listener)

  def tick(self):
    log(self, " Tick")
    if not self.hasFinished():
      # Cleanup the old status before executing the change
      self._clearStatus()
      # Increment the number of ticks in this letter
      self._characterSequence.next()
      # Move the motor sequence
      self._motorSequence.next()
      # Update the current system status
      self._publishStatus()

  def hasFinished(self):
    return self._characterSequence.isMatching(self._targetLetter)

  def setTarget(self, letter):
    if letter not in self._characterSequence:
      raise Exception("Invalid target letter: " + str(letter) + " not present on this character")
    log(self, "Setting target: " + letter)
    self._targetLetter = letter

  def _getCurrentLetter(self):
    return self._characterSequence.getValue()

  def _setNextLetter(self):
    self._characterSequence.next()
    log(self, "Setting letter: " + self._getCurrentLetter())

  def logId(self):
    return "Character - " + str(self._motorId)

class _Reporter:
  def __init__(self, motorId, characterSequence, listener):
    self._listener = listener
    self._characterSequence = characterSequence
    self._motorId = motorId

  def forMotorSequenceIndex(self, sequenceId):
    self._sequenceId = sequenceId
    self._characterSequence.inform(self.forCharacterSequenceIndex)

  def forCharacterSequenceIndex(self, characterSequenceIndex):
    self._listener.set(self._motorId, characterSequenceIndex, self._sequenceId)

# This class will keep track of where we are standing on a character.
# A logical representation of a character is made by two components:
# - Letters represented: [A, B, C, D]
# - Motor step index to each letter: [5, 7, 10, 11]
# With this example, the character would be showing the letter A from the logical 0 till 5 ticks, B from 5-7, etc.
# Ideally, each letter should take the same amount of steps to turn, but this was not the case with the one I built.
# This class will take this data, and represent it as a circular list, for example:
#          [A, A, A, A, A, A, B, B, C, C, C, D]
# and after the last D, it will cycle back to A (that is what the physical character should be showing)
class StartPointCharacterSequence:
  def __init__(self, charId, possibleValues, indexChanges, currentIndex):
    log(self, " creating from values: " + str(possibleValues) + " and changes: " + str(indexChanges))
    self._motorSequence = []
    self._id = charId
    self._populateSequence(possibleValues, indexChanges)
    self._currentIndex = currentIndex

  def _populateSequence(self, possibleValues, indexChanges):
    appendingIndex = 0
    valueIndex = 0
    for index in indexChanges:
      for _ in range(index - appendingIndex):
        self._motorSequence.append(possibleValues[valueIndex])
        appendingIndex = appendingIndex + 1
      valueIndex = valueIndex + 1

  def next(self):
    self._currentIndex = self._currentIndex + 1
    if self._currentIndex >= len(self._motorSequence):
      self._currentIndex = 0
    log(self, "Setting index: " + str(self._currentIndex))

  def inform(self, listener):
    listener(self._currentIndex)

  def isMatching(self, value):
    return self._getLetter() == value

  def _getLetter(self):
    return self._motorSequence[self._currentIndex]

  def __contains__(self, key):
    return key in self._motorSequence

  def logId(self):
    return "Character Sequence - " + str(self._id)

# This character sequence will only accept it is showing a value when the letter is close to the half of it's interval.
# For example:
#             If letter B starts at 40 and goes until 100, at 40 the character should be showing letter B, but
#             this sequence won't acknowledge it. It will only acknowledge when the ticks are at 64-76 (the 40%-60% range).
# This will be of use when the limits are kind of diffuse, since the midpoint interval inside the letter range should always be
# a safe bet that the letter is being shown.
class MidPointCharacterSequence:
  def __init__(self, charId, possibleValues, indexChanges, currentIndex):
    log(self, " creating from values: " + str(possibleValues) + " and changes: " + str(indexChanges))
    self._id = charId
    self._currentIndex = currentIndex
    self._tokens = possibleValues
    self._indexChanges = indexChanges

  def next(self):
    self._currentIndex = self._currentIndex + 1
    if self._currentIndex > self._indexChanges[-1]:
      self._currentIndex = 0
    log(self, "Setting index: " + str(self._currentIndex))

  def inform(self, listener):
    listener(self._currentIndex)

  def isMatching(self, value):
    return self._getLetter() == value

  def _getLetter(self):
    index = 0
    while self._indexChanges[index] < self._currentIndex:
      index = index + 1

    if index == 0:
      lowerPoint = 0
    else:
      lowerPoint = self._indexChanges[index - 1]
    higherPoint = self._indexChanges[index]
    delta = higherPoint - lowerPoint
    targetIntervalRange = delta * 0.4

    if self._currentIndex > lowerPoint + targetIntervalRange and self._currentIndex < higherPoint - targetIntervalRange:
      return self._tokens[index]
    else:
      return None

  def __contains__(self, key):
    return key in self._tokens

  def logId(self):
    return "Character Midpoint Sequence - " + str(self._id)
