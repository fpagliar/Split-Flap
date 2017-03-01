
def buildShiftRegistry(dataPin, clockPin, shiftPin, timer, sequences):
  controller = _ShiftRegistryController(dataPin, clockPin, shiftPin, timer)
  registry = _ShiftRegistry(controller, len(sequences) * 4)
  return SequenceManager(sequences, registry)

class SequenceManager:
  def __init__(self, sequences, listener):
    self._sequences = sequences
    self._registry = listener
  
  def publish(self):
    currentStatuses = [x.current() for x in self._sequences]
    binaryRepresentation = sum(currentStatuses, [])
    pinRepresentation = [x == 1 for x in binaryRepresentation]
    self._registry.set(pinRepresentation)

class _ShiftRegistry:
  def __init__(self, controller, length):
    self._controller = controller
    self._length = length

  def set(self, binary):
    if len(binary) != self._length: 
      raise Exception("The shift registry provided has size:" + str(self._length) + " and can't represent output: " + str(binary))
      
    for val in binary:
      self._controller.send(val)
    self._controller.publish()
    
class _ShiftRegistryController:
  def __init__(self, dataPin, clockPin, shiftPin, timer):
    self._dataPin = dataPin
    self._clockPin = clockPin
    self._shiftPin = shiftPin
    self._timer = timer

  def send(self, isActive):
    self._dataPin.set(isActive)
    self._tick()
  
  def _tick(self):
    self._clockPin.on()
    self._timer.waitRegistryClockPulse()
    self._clockPin.off()
  
  def publish(self):
    self._shiftPin.on()
    self._timer.waitRegistryPublishPulse()
    self._shiftPin.off()
