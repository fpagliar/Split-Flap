import time
from Logger import log

# This class represents the whole display. That display is composed by a group of characters.
# It receives the characters (that are a logical representation of what the physical one is showing) and a listener
# that will take care of the logic of how to publish the current system state.
class Display:
  def __init__(self, characters, publisher):
    self._characters = characters
    self._publisher = publisher

  def show(self, message):
    log(self, "Showing: " + message)
    self.setTarget(message)
    self.run()

  def run(self):
    while not self.hasFinished():
      self._tick()
      time.sleep(1)  # TODO: remove, just to go slow for testing

  def _tick(self):
    log(self, "Tick")
    for char in self._characters:
      if not char.hasFinished():
        char.tick()
    self._publisher.publish()

  def setTarget(self, message):
    log(self, "Setting target: " + message)
    for i in range(0, len(self._characters)):
      if i < len(message):
        self._characters[i].setTarget(message[i])

  def getCurrentString(self):
    return "".join([elem.getCurrentLetter() for elem in self._characters])

  def hasFinished(self):
    return all([elem.isReady() for elem in self._characters])

  def logId(self):
    return "Display"
