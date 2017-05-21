from Configuration import SystemConfiguration


config = SystemConfiguration()
_textPins = {}
_loggerPins = {}

if not config.shouldUseTextPins():
  import RPi.GPIO as GPIO
  GPIO.setmode(GPIO.BCM)

# Main interface method that provides the correct pin instance to the context that requires it.
def GetPin(pinId):
  if pinId not in _textPins:
    if config.shouldUseTextPins():
      _textPins[pinId] = _TextBasedPin(pinId)
    else:
      _textPins[pinId] = _RaspyPin(pinId)
  return _textPins[pinId]

def GetLoggerPin(pinId, logger):
  if pinId not in _loggerPins:
    _loggerPins[pinId] = _LoggerPin(pinId, logger)
  return _loggerPins[pinId]

class _LoggerPin:
  def __init__(self, pin, logger):
    self._id = pin.getId()
    self._pin = pin
    self._logger = logger

  def set(self, active):
    self._logger.log(self._id, active)
    self._pin.set(active)

  def on(self):
    self.set(True)

  def off(self):
    self.set(False)

# Simulates a pin with the same interface, but in practice just logs the values to the console
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

  def __str__(self):
    return str(self.id)

# Represents a raspberry pi pin that will offer a simple interface to manipulate it
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

