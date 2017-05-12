from Logger import log
from Configuration import Keywords

def buildConnection(config, buildPinFor, length, timer):
    isDirectConnection = config.get(Keywords.USE_DIRECT_CONNECTION)
    if isDirectConnection:
#         pinIds = config.get(Keywords.SEQUENCE_PINS)
#         pins = [buildPinFor(pinIds[i]) for i in range(len(pinIds))]
        pins = [buildPinFor(pin) for pin in config.get(Keywords.SEQUENCE_PINS)]
        if length > len(pins):
            raise Exception("Can't create a direct connection of " + str(length) + " not enough pins")
        return _DirectConnection(pins[:length * 4]) # Each motor uses 4 pins
    else:
        dataPin = buildPinFor(config.get(Keywords.DATA_PIN))
        clockPin = buildPinFor(config.get(Keywords.CLOCK_PIN))
        shiftPin = buildPinFor(config.get(Keywords.SHIFT_PIN))
        controller = _ShiftRegistryController(dataPin, clockPin, shiftPin, timer)
        return _ShiftRegistry(controller, length)

# This class will make the abstraction of relating sequences to connections.
# It has only one method that is publish, and will transmit the current system status through the connections.
# That is, if we have motor 1 on step 0101 and motor 2 on step 1100, it's objective is to push through the connection the 
# value 01011100.
class SequencePublisher:
  def __init__(self, sequences, listener):
    self._sequences = sequences
    self._listener = listener
  
  def publish(self):
    log(SequencePublisher.__name__, "Sequence Publisher", "Publishing sequences: " + "\n".join([str(x) for x in self._sequences]))
    currentStatuses = [x.current() for x in self._sequences]
    binaryRepresentation = sum(currentStatuses, [])
    pinRepresentation = [x == 1 for x in binaryRepresentation]
    self._listener.set(pinRepresentation)

# This class is used to represent sequence inputs being directly connected to the GPIO pins.
# In this case, to show the sequence we want, we only need to set the corresponding pins to the same value.
# The caller can be agnostic on how the wiring is made, and just invoke set(010100) and let this instance figure it out.
class _DirectConnection:
  def __init__(self, inputPins):
    log(_DirectConnection.__name__, "Direct Connection", "Creating direct connection for pins:" + str(inputPins))
    self._inputs = inputPins

  def set(self, binary):
    if len(binary) != len(self._inputs):
      raise Exception("Can't publish over direct connection the sequence. Sequence len: " + str(len(binary)) + " | inputs len:" + str(len(self._inputs)))
    for i in range(len(binary)):
      self._inputs[i].set(binary[i])

# This class represents a logical view of a ShiftRegistry. The user of this class, can be agnostic of how a shift registry works 
# in reality, it just invokes set(000100010) and let the class handle the hardware part.
# It receives a controller, that will know how to set each bit.
class _ShiftRegistry:
  def __init__(self, controller, length):
    log(_ShiftRegistry.__name__, "Shift registry", "Creating shift registry of length:" + str(length))
    self._controller = controller
    self._length = length

  def set(self, binary):
    if len(binary) != self._length: 
      raise Exception("The shift registry provided has size:" + str(self._length) + " and can't represent output: " + str(binary))
      
    for val in binary:
      self._controller.send(val)
    self._controller.publish()

# This class represents the basic logic on how a shift registry works on a hardware level.
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
    self._timer.waitBetweenMotorSequences()
