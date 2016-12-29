
class TextBasedPin:
  def __init__(self, pinNumber):
    self.id = pinNumber
    print("Setup pin: " + str(pinNumber))
    
  def set(self, active):
    if active:
      print(str(self.id) + " Activated")
    else:
      print(str(self.id) + " Deactivated")
    
  def on(self):
    self.set(True)

  def off(self):
    self.set(False)
