import time
from datetime import datetime
from datetime import timedelta

class MotorController:
  def __init__(self, length, properties):
    self.latestUpdateTime = {}
    self._properties = properties
    listOfPins = properties.PINS[:length]
    self.idToMotorInfo = {listOfPins.index(i): _MotorInfo(i, properties) for i in listOfPins}

  def tick(self, pinId):
    # First, make sure that we are not sending messages too fast to this component
    self._validateTime(pinId)
    # Turn all power pins off   
    motorInfo = self.idToMotorInfo[pinId]
    # Set the sequence
    print("Setting seq " + ' '.join(map(str, motorInfo.nextSequence())))
    # Turn the pin we need on
    print("Turn on pin " + str(motorInfo.getPin()))
    
  def _validateTime(self, pinId):
    if pinId in self.latestUpdateTime:
      last = self.latestUpdateTime[pinId]
      if last + timedelta(milliseconds=4) > datetime.now():
        print("sleeping")
        time.sleep(0.04)
    self.latestUpdateTime[pinId] = datetime.now()
    
class _MotorInfo:
  def __init__(self, pin, properties):
    self.pin = pin
    self._properties = properties
    self.sequenceIndex = 0

  def getPin(self):
    return self.pin
  
  def nextSequence(self):
    current = self.sequenceIndex
    self.sequenceIndex = self.sequenceIndex + 1
    if self.sequenceIndex == len(self._properties.MOTOR_SEQUENCE):
      self.sequenceIndex = 0
    return self._properties.MOTOR_SEQUENCE[current]