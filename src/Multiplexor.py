
class FourTo16Multiplexor:
  def __init__(self, outputPins, powerPin):
    self.outputs = outputPins
    self.power = powerPin

  def turnOn(self):
    self.power.on()
    
  def turnOff(self):
    self.power.off()

  def set(self, outputId):
    values = self._getMultiplexorActivationValues(outputId)
    for i in range(len(self.outputs)):
      self.outputs[i].set(values[i])

  def _getMultiplexorActivationValues(self, outputId):
    ans = [False] * 16
    ans[outputId] = True
    return ans
    
    # bin will give the number in binary string, we trail the leading '0b' prefix,
    # and then convert to a boolean representing if it should be turned on or off
#     return [x == '1' for x in bin(outputId)[2:]]
