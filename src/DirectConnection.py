from Logger import log

class DirectConnection:
  def __init__(self, inputPins, sequence):
    log("Creating direct connection for pins:" + str(inputPins))
    self._inputs = inputPins
    self._sequence = sequence

  def publish(self):
    current = self._sequence.current()
    log("Publishing sequence: " + str(self._sequence))
    if len(current) != len(self._inputs):
      raise Exception("Can't publish over direct connection the sequence. Sequence len: " + len(current) + " | inputs len:" + len(self._inputs))
    for i in range(len(current)):
      self._inputs[i].set(current[i])