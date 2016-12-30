
class Multiplexor:
  def __init__(self, inputPins, powerPin):
    self._inputs = inputPins
    self._power = powerPin

  def on(self):
    self._power.on()
    
  def off(self):
    self._power.off()

  def set(self, outputId):
    self._validateOutputId(outputId)
    values = self._getMultiplexorActivationValues(outputId)
    for i in range(len(self._inputs)):
      self._inputs[i].set(values[i])
  
  def _validateOutputId(self, outputId):
    size = len(self._inputs)
    if outputId <= 0 or outputId > 2 ** size:
      raise Exception("The multiplexor provided has size:" + str(size) + " and can't represent output: " + str(outputId))

  def _getMultiplexorActivationValues(self, outputId):
    # The format will turn the number to binary, and fill up with leading zeroes
    fmt = '0' + str(len(self._inputs)) + 'b'
    return [x == '1' for x in format(outputId - 1, fmt)]
    
