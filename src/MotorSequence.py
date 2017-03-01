from Logger import log

class MotorSequence:
  def __init__(self, sequence, currentIndex=0):
    self._sequence = sequence
    self._currentIndex = currentIndex
    log("Creating motor sequence with index:" + str(self._currentIndex))
    
  def next(self):
    self._currentIndex += 1
    self._currentIndex %= len(self._sequence)
    log("Moving the sequence to step:" + str(self._currentIndex))
        
  def current(self):
    return self._sequence[self._currentIndex]
  
  def currentIndex(self):
    return self._currentIndex
  
  def __str__(self):
    return str(self.currentIndex()) + ": " + str(self.current())
