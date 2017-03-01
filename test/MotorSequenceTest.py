import unittest
from MotorSequence import MotorSequence
from unittest import mock

class MotorSequenceTest(unittest.TestCase):

  def createSequence(self):
      sequence = [['A', 'B', 'C', 'D'],
                  [1, 2, 3, 4],
                  [True, True, True, False],
                ]
      return sequence, MotorSequence(sequence)

  def test_starts_with_the_first_sequence(self):
    sequence, motorSequence = self.createSequence()
    self.assertEqual(sequence[0], motorSequence.current())
      
  def test_next_moves_sequence(self):
    sequence, motorSequence = self.createSequence()
    motorSequence.next()
    self.assertEqual(sequence[1], motorSequence.current())

  def test_next_gets_to_first_value_after_last(self):
    sequence, motorSequence = self.createSequence()
    for _ in range(len(sequence)):
      motorSequence.next()
    self.assertEqual(sequence[0], motorSequence.current())
    
if __name__ == '__main__':
    unittest.main()
