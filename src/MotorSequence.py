from Logger import log

# This class represents the sequence on a stepper motor.
# The constructor gets the sequence that is configured for this specific type of motor, and provides methods
# to navigate with it.
class MotorSequence:
  def __init__(self, id, sequence, currentIndex = 0):
    self._sequence = sequence
    self._currentIndex = currentIndex
    self._id = id
    log(MotorSequence.__name__, "Motor Sequence #" + str(self._id), "Creating motor sequence with index:" + str(self._currentIndex))

  def next(self):
    self._currentIndex += 1
    self._currentIndex %= len(self._sequence)
    log(MotorSequence.__name__, "Motor Sequence #" + str(self._id), "Moving the sequence to step:" + str(self._currentIndex))

  def current(self):
    return self._sequence[self._currentIndex]

  def _currentIndex(self):
    return self._currentIndex

  def __str__(self):
    return str(self._currentIndex()) + ": " + str(self.current())
