import unittest
from MotorController import MotorController
from unittest import mock

class MotorControllerTest(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(MotorControllerTest, self).__init__(*args, **kwargs)
    self._numberOfMotors = 4
  
  def setupController(self):
    sequences = [mock.Mock(name = "Motor" + str(i)) for i in range(self._numberOfMotors)]
    builder = mock.Mock()
    builder.build.side_effect = sequences
    motorCommunicator = mock.Mock(name = "MotorCommunicator")
    return sequences, motorCommunicator, MotorController(self._numberOfMotors, motorCommunicator, builder.build)

  def test_tick_first_should_increment_that_squence(self):
    sequences, _, controller = self.setupController()
    controller.tick(1)
    sequences[0].next.assert_called_once_with()

  def test_tick_first_should_not_increment_other_squences(self):
    sequences, _, controller = self.setupController()
    controller.tick(1)
    for seq in sequences[1:]:
      seq.next.assert_not_called()

  def test_tick_last_should_increment_that_squence(self):
    sequences, _, controller = self.setupController()
    last = len(sequences)
    controller.tick(last)
    sequences[last - 1].next.assert_called_once_with()

  def test_tick_last_should_not_increment_other_squences(self):
    sequences, _, controller = self.setupController()
    last = len(sequences)
    controller.tick(last)
    for seq in sequences[:-1]:
      seq.next.assert_not_called()
  
  def test_tick_calls_the_communicator_with_the_first_motorId(self):
    self.checkCommunicatorCalledWithCorrectMotorId(1)

  def test_tick_calls_the_communicator_with_the_second_motorId(self):
    self.checkCommunicatorCalledWithCorrectMotorId(2)
  
  def test_tick_calls_the_communicator_with_the_last_motorId(self):
    self.checkCommunicatorCalledWithCorrectMotorId(self._numberOfMotors - 1)

  def checkCommunicatorCalledWithCorrectMotorId(self, index):
    _, communicator, controller = self.setupController()
    controller.tick(index)
    communicator.send.assert_called_once_with(index, mock.ANY)
  
  def test_tick_calls_the_communicator_with_the_first_sequence(self):
    self.checkCommunicatorCallForMotor(1)

  def test_tick_calls_the_communicator_with_the_second_sequence(self):
    self.checkCommunicatorCallForMotor(2)

  def test_tick_calls_the_communicator_with_the_last_sequence(self):
    self.checkCommunicatorCallForMotor(self._numberOfMotors - 1)
    
  def checkCommunicatorCallForMotor(self, index):
    sequences, communicator, controller = self.setupController()
    controller.tick(index)
    communicator.send.assert_called_once_with(mock.ANY, sequences[index - 1])

if __name__ == '__main__':
    unittest.main()
