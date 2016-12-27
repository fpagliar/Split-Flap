from MotorController import MotorController
from Display import SetupDisplay
import Utils
from Character import CreateCharacter
from Properties import Properties

def testRun():
  disp = SetupDisplay(CreateCharacter, 4, Properties())
  disp.show("CBDD")
  disp.show("ABD")

def validateParam():
  motor = MotorController(1)
  print("Please check when the next letter shows up on the first character")
  while not Utils.askForConfirmation("Is it shown yet?"):
    motor.tick(1)
  print("Great! Now, we'll do a step by step to figure out how many turns are needed to pass each letter")
  i = 0
  while not Utils.askForConfirmation("Is it the next letter already?"):
    i = i+1
    motor.tick(1)
  print("The number of tiks per letter is:" + str(i))

if __name__ == "__main__":
  testRun()