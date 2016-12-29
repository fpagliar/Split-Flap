import RPi.GPIO as GPIO

class RaspyPin:
  def __init__(self, pinNumber):
    self.id = pinNumber
    GPIO.setup(self.id, GPIO.OUT)
    
  def set(self, active):
    GPIO.output(self.id, active)
    
  def on(self):
    self.set(True)

  def off(self):
    self.set(False)
