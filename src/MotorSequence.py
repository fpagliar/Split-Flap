
class MotorSequence:
  def __init__(self, sequence, currentIndex=0):
    self._sequence = sequence
    self._currentIndex = currentIndex
    
  def next(self):
    self._currentIndex += 1
    self._currentIndex %= len(self._sequence)
        
  def current(self):
    return self._sequence[self._currentIndex]
  
  def currentIndex(self):
    return self._currentIndex
  
  def __str__(self):
    return self.currentIndex()
