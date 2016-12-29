import unittest
from Multiplexor import FourTo16Multiplexor
from unittest import mock

class MultiplexorTest(unittest.TestCase):

  def createMultiplex(self):
    power = mock.Mock(name = "Power")
    outputPins = []
    for i in range(16):
      outputPins.append(mock.Mock(name = i))
    multiplex = FourTo16Multiplexor(outputPins, power)
    return multiplex, outputPins, power

  def test_turnOff_turns_power_off(self):
    multiplex, _, power = self.createMultiplex()
    multiplex.turnOff()
    power.off.assert_called_once_with()

  def test_turnOn_turns_power_on(self):
    multiplex, _, power = self.createMultiplex()
    multiplex.turnOn()
    power.on.assert_called_once_with()
    
  def test_set_zero_sets_only_the_first_bit(self):
    multiplex, outputPins, _ = self.createMultiplex()
    multiplex.set(0)
    outputPins[0].set.assert_called_once_with(True)
    for pin in outputPins[1:]:
      pin.set.assert_called_once_with(False)

  def test_set_fifteen_sets_only_the_last_bit(self):
    multiplex, outputPins, _ = self.createMultiplex()
    multiplex.set(15)
    outputPins[-1].set.assert_called_once_with(True)
    for pin in outputPins[:-1]:
      pin.set.assert_called_once_with(False)

if __name__ == '__main__':
    unittest.main()
