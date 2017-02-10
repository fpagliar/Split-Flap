
class DirectConnection:
  def __init__(self, inputPins):
    self._inputs = inputPins

  def on(self):
    pass
    
  def off(self):
    pass

  def set(self, outputId):
    for i in range(len(self._inputs)):
      self._inputs[i].set(i == outputId)