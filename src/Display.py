import time

class Display:
  def __init__(self, characters, shiftRegistry):
    self._characters = characters
    self._shiftRegistry = shiftRegistry
    self._index = 0
    
  def show(self, message):
    self.setTarget(message)
    self.run()
  
  def run(self):
    while not self.hasFinished():
      self.tick()
      time.sleep(1) # TODO: remove, just to go slow for testing
      
  def tick(self):
    if not self.hasFinished():
      self._characters[self._index].tick()
      self._index +=1
      self._index %= len(self._characters)
    self._shiftRegistry.publish()

  def setTarget(self, message):
    for i in range(0, len(self._characters)):
      if i < len(message):
        self._characters[i].setTarget(message[i])

  def getCurrentStatus(self):
    return [elem.getCurrentStatus() for elem in self._characters]

  def getCurrentString(self):
    return "".join([elem.getCurrentLetter() for elem in self._characters])

  def getCurrentIndex(self):
    return self._index
    
  def hasFinished(self):
    return all([elem.isReady() for elem in self._characters])