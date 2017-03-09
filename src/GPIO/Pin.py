import RPi.GPIO as GPIO

_pins = {}

GPIO.setmode (GPIO.BCM)

def GetPin(pinId):
  if pinId not in _pins:
    _pins[pinId] = _RaspyPin(pinId)
  return _pins[pinId]  

class _RaspyPin:
  def __init__(self, pinNumber):
    self.id = pinNumber
    GPIO.setup(self.id, GPIO.OUT)
    
  def set(self, active):
    GPIO.output(self.id, active)
    
  def on(self):
    self.set(True)

  def off(self):
    self.set(False)
