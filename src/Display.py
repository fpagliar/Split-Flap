import time
from MotorController import MotorController
import Utils

def SetupDisplay(Character, length, properties):
  controller = MotorController(length, properties)
  characters = [Character(i, controller, properties) for i in range(0, length)]
  print("Spin all the flaps to show the letter A")
  for i in range (0, len(characters)):
    configured = False
    print("Now configuring the character " + str(i + 1))
    characters[i].setTarget("B")
    while not configured:
      characters[i].tick()
      print(characters[i].getCurrentLetter())
      configured = Utils.askForConfirmation("Is it showing letter B now?")
  return Display(characters, properties)

class Display:
  def __init__(self, characters):
    self._characters = characters
    
  def show(self, message):
    for i in range(0, len(self._characters)):
      if i < len(message):
        self._characters[i].setTarget(message[i])
    
    while not self.hasFinished():
      for character in self._characters:
        character.tick()
      
      print("CURRENT STATUS " + self.getCurrentString())
      time.sleep(1)

  def getCurrentString(self):
    return "".join([elem.getCurrentLetter() for elem in self._characters])
    
  def hasFinished(self):
    return all([elem.isReady() for elem in self._characters])