
_pins = {}

def GetPin(pinId):
  if pinId not in _pins:
    _pins[pinId] = _TextBasedPin(pinId)
  return _pins[pinId]  

class _TextBasedPin:
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

