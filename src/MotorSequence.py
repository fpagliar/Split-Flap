

class MotorSequence:
  def __init__(self, listeners, sequence):
    self._listeners = listeners
    self._sequence = sequence
    self._currentIndex = 0
    
  def next(self):
    self._currentIndex = self._currentIndex + 1
    if self._currentIndex == len(self._sequence):
      self._currentIndex = 0
      
  def apply(self):
    for i in range(0, len(self._listeners)):
      self._listeners[i].set(self.current()[i])
      
  def current(self):
    return self._sequence[self._currentIndex]
