import unittest
from ShiftRegistry import _ShiftRegistryController, _ShiftRegistry, SequenceManager
from unittest import mock

class ShiftRegistryTest(unittest.TestCase):

  # Shift registry controller tests

  def createController(self):
    data = mock.Mock(name = "Data")
    clock = mock.Mock(name = "Clock")
    shift = mock.Mock(name = "Shift")
    timer = mock.Mock(name = "Timer")
    return data, clock, shift, timer, _ShiftRegistryController(data, clock, shift, timer)

  def test_send_sets_pin_to_Up(self):
    data, _, _, _, controller = self.createController()
    controller.send(True)
    data.set.assert_called_once_with(True)

  def test_send_sets_pin_to_Down(self):
    data, _, _, _, controller = self.createController()
    controller.send(False)
    data.set.assert_called_once_with(False)

  def test_send_up_sends_pulse(self):
    _, clock, _, timer, controller = self.createController()
    controller.send(True)
    clock.on.assert_called_once_with()
    timer.waitRegistryClockPulse.test_assert_called_once_with()
    clock.off.assert_called_once_with()

  def test_send_down_sends_pulse(self):
    _, clock, _, timer, controller = self.createController()
    controller.send(False)
    clock.on.assert_called_once_with()
    timer.waitRegistryClockPulse.test_assert_called_once_with()
    clock.off.assert_called_once_with()

  def test_publish_sends_shift(self):
    _, _, publish, timer, controller = self.createController()
    controller.publish()
    publish.on.assert_called_once_with()
    timer.waitRegistryPublishPulse.test_assert_called_once_with()
    publish.off.assert_called_once_with()

  # Shift registry tests

  def createShiftRegistry(self):
    controller = mock.Mock(name = "controller")
    length = 10
    return controller, length, _ShiftRegistry(controller, length)

  def test_set_zeros(self):
    controller, length, registry = self.createShiftRegistry()
    registry.set([False] * length)
    controller.send.assert_called_with(False)
    assert controller.send.call_count == length

  def test_set_ones(self):
    controller, length, registry = self.createShiftRegistry()
    registry.set([True] * length)
    controller.send.assert_called_with(True)
    assert controller.send.call_count == length

  def test_set_any_publishes(self):
    controller, length, registry = self.createShiftRegistry()
    registry.set([True] * length)
    controller.publish.assert_called_once_with()
    
  def test_set_short_array_fails(self):
    _, length, registry = self.createShiftRegistry()
    with self.assertRaises(Exception):
      registry.set([True] * length - 1)

  def test_set_long_array_fails(self):
    _, length, registry = self.createShiftRegistry()
    with self.assertRaises(Exception):
      registry.set([True] * length + 1)
    
  # Sequence Manager tests
  
  def createSequenceManger(self):
    length = 5
    sequences = []
    for i in range(length):
      seq = mock.Mock(name = "Sequence" + str(i))
      seq.current.return_value = []
      sequences.append(seq)
    registry = mock.Mock(name = "Registry")
    return sequences, registry, SequenceManager(sequences, registry)
  
  def test_publish_calls_the_registry(self):
    _, registry, manager = self.createSequenceManger()
    manager.publish()
    registry.set.test_assert_called_with_any()

  def test_publish_calls_with_the_current_statuses(self):
    sequences, registry, manager = self.createSequenceManger()
    statuses = [[1, 0, 0], [1, 1, 1], [], [], [0, 0, 0]]
    for i in range(len(statuses)):
      sequences[i].current.return_value = statuses[i]
    manager.publish()
    registry.set.test_assert_called_with([1, 0, 0, 1, 1, 1, 0, 0, 0])

if __name__ == '__main__':
    unittest.main()
