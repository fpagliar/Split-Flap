import unittest
from Multiplexor import Multiplexor
from unittest import mock

class MultiplexorTest(unittest.TestCase):

  def createMultiplex(self):
    power = mock.Mock(name = "Power")
    inputPins = []
    for i in range(4):
      inputPins.append(mock.Mock(name = i))
    multiplex = Multiplexor(inputPins, power)
    return multiplex, inputPins, power

  def test_turnOff_turns_power_off(self):
    multiplex, _, power = self.createMultiplex()
    multiplex.off()
    power.off.assert_called_once_with()

  def test_turnOn_turns_power_on(self):
    multiplex, _, power = self.createMultiplex()
    multiplex.on()
    power.on.assert_called_once_with()
    
  def test_set_four_sets_0011(self):
    multiplex, inputPins, _ = self.createMultiplex()
    multiplex.set(4)
    for pin in inputPins[:2]:
      pin.set.assert_called_once_with(False)
    for pin in inputPins[2:]:
      pin.set.assert_called_once_with(True)

  def test_set_one_sets_all_zeroes(self):
    multiplex, inputPins, _ = self.createMultiplex()
    multiplex.set(1)
    for pin in inputPins:
      pin.set.assert_called_once_with(False)

  def test_set_sixteen_sets_all_ones(self):
    multiplex, inputPins, _ = self.createMultiplex()
    multiplex.set(16)
    for pin in inputPins:
      pin.set.assert_called_once_with(True)

  def test_set_seventeen_raises_error(self):
    multiplex, _, _ = self.createMultiplex()
    with self.assertRaises(Exception):
      multiplex.set(17)

  def test_set_zero_raises_error(self):
    multiplex, _, _ = self.createMultiplex()
    with self.assertRaises(Exception):
      multiplex.set(0)

if __name__ == '__main__':
    unittest.main()
