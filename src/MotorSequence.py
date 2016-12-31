
class MotorSequence:
  def __init__(self, listeners, sequence, currentIndex=0):
    self._listeners = listeners
    self._sequence = sequence
    self._currentIndex = currentIndex
    
  def next(self):
    self._currentIndex += 1
    self._currentIndex %= len(self._sequence)
      
  def apply(self):
    for i in range(0, len(self._listeners)):
      self._listeners[i].set(self.current()[i])
      
  def current(self):
    return self._sequence[self._currentIndex]
  
  def currentIndex(self):
    return self._currentIndex
  
  def __str__(self):
    return self.currentIndex()
