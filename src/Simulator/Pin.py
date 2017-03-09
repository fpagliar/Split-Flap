
_textPins = {}
_loggerPins = {}

def GetPin(pinId):
  if pinId not in _textPins:
    _textPins[pinId] = _TextBasedPin(pinId)
  return _textPins[pinId]  

def GetLoggerPin(pinId, logger):
  if pinId not in _loggerPins:
    _loggerPins[pinId] = _LoggerPin(pinId, logger)
  return _loggerPins[pinId]  

class _LoggerPin:
  def __init__(self, pinNumber, logger):
    self._id = pinNumber
    self._logger = logger
    
  def set(self, active):
    self._logger.log(self._id, active)

  def on(self):
    self.set(True)

  def off(self):
    self.set(False)


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

