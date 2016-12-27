import unittest
from Display import Display
from unittest import mock
from Properties import Properties

class DisplayTest(unittest.TestCase):

  def test_show_message_sets_letter_to_characters(self):
    message = "ABCDEFG"
    characters = [mock.Mock(name = message[i]) for i in range(0, len(message))]
    display = Display(characters, Properties())
    display.show(message)
    for i in range(0, len(message)):
      characters[i].setTarget.assert_called_once_with(message[i])
      
  def test_get_message_shows_current_value_instead_of_target(self):
    message = "ABCDEF"
    characters = [mock.Mock(name = message[i]) for i in range(0, len(message))]
    current = "AABBCC"
    for i in range(0, len(message)):
      characters[i].getCurrentLetter.return_value = current[i]
    display = Display(characters, Properties())
    display.show(message)
    self.assertEqual(current, display.getCurrentString())
    
  def setupHasFinishedTest(self, results):
    message = "A" * len(results)
    characters = [mock.Mock(name = message[i]) for i in range(0, len(message))]
    display = Display(characters, Properties())
    display.show(message)
    for i in range(0, len(results)):
      characters[i].isReady.return_value = results[i]
    return display
    
  def test_has_finished_if_all_chars_finished(self):
    display = self.setupHasFinishedTest([True, True, True])
    self.assertTrue(display.hasFinished())

  def test_has_not_finished_if_no_chars_finished(self):
    display = self.setupHasFinishedTest([False, False, False])
    self.assertFalse(display.hasFinished())

  def test_has_not_finished_if_one_char_not_finished(self):
    display = self.setupHasFinishedTest([True, True, True, False])
    self.assertFalse(display.hasFinished())

if __name__ == '__main__':
    unittest.main()