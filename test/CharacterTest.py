import unittest
from Character import Character
from unittest import mock
from Properties import Properties

class CharacterTest(unittest.TestCase):

  def test_character_starts_with_A(self):
    char = Character(1, mock.Mock(), Properties())
    self.assertEquals(char.getCurrentLetter(), 'A')

  def test_setting_a_target_does_not_change_current_letter(self):
    char = Character(1, mock.Mock(), Properties())
    current = char.getCurrentLetter()
    char.setTarget('Z')
    self.assertEquals(current, char.getCurrentLetter())

  def test_new_target_different_from_current_is_not_ready(self):
    char = Character(1, mock.Mock(), Properties())
    char.setTarget('Z')
    self.assertFalse(char.isReady())

  def test_it_takes_config_ticks_to_change_a_letter(self):
    char = Character(1, mock.Mock(), Properties())
    current = char.getCurrentLetter()
    char.setTarget('Z')
    self.assertFalse(char.isReady())
    char.tick()
    self.assertEquals(current, char.getCurrentLetter())
    
  def test_less_than_config_ticks_does_not_change_the_letter(self):
    properties = Properties()
    char = Character(1, mock.Mock(), properties)
    current = char.getCurrentLetter()
    char.setTarget('Z')
    self.assertFalse(char.isReady())
    for _ in range(0, properties.TICKS_PER_LETTER - 1):
      char.tick()
    self.assertEquals(current, char.getCurrentLetter())

  def test_config_tick_changes_the_letter_if_not_ready(self):
    properties = Properties()
    char = Character(1, mock.Mock(), properties)
    current = char.getCurrentLetter()
    char.setTarget('Z')
    self.assertFalse(char.isReady())
    for _ in range(0, properties.TICKS_PER_LETTER):
      char.tick()
    self.assertNotEquals(current, char.getCurrentLetter())

  def test_config_tick_does_not_change_the_letter_if_ready(self):
    properties = Properties()
    char = Character(1, mock.Mock(), properties)
    current = char.getCurrentLetter()
    char.setTarget('A')
    self.assertTrue(char.isReady())
    for _ in range(0, properties.TICKS_PER_LETTER):
      char.tick()
    self.assertEquals(current, char.getCurrentLetter())

  def test_char_is_ready_when_the_target_is_reached(self):
    properties = Properties()
    char = Character(1, mock.Mock(), properties)
    char.setTarget('B')
    self.assertFalse(char.isReady())
    for _ in range(0, properties.TICKS_PER_LETTER):
      char.tick()
    self.assertTrue(char.isReady())
    self.assertEquals('B', char.getCurrentLetter())
    
  def test_run_once_informs_controller(self):
    controller = mock.Mock()
    properties = Properties()
    char = Character(1, controller, properties)
    char.setTarget('B')
    char.tick()
    controller.tick.assert_called_once_with(1)

  def test_run_informs_controller_every_tick(self):
    controller = mock.Mock()
    properties = Properties()
    char = Character(1, controller, properties)
    current = char.getCurrentLetter()
    char.setTarget('Z')
    self.assertFalse(char.isReady())
    for _ in range(0, properties.TICKS_PER_LETTER):
      char.tick()
    self.assertNotEquals(current, char.getCurrentLetter())
    controller.tick.assert_called_with(1)

  def test_run_does_not_inform_controller_if_ready(self):
    controller = mock.Mock()
    properties = Properties()
    char = Character(1, controller, properties)
    self.assertTrue(char.isReady())
    for _ in range(0, properties.TICKS_PER_LETTER):
      char.tick()
    controller.tick.assert_not_called()

if __name__ == '__main__':
    unittest.main()
