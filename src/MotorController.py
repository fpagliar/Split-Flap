import time
from datetime import datetime
from datetime import timedelta

class MotorController:
  def __init__(self, numberOfMotors, motorCommunicator, sequenceBuilder):
    self._latestUpdateTime = {}
    self._numberOfMotors = numberOfMotors
    self._motorCommunicator = motorCommunicator
    self._sequences = [sequenceBuilder() for _ in range(numberOfMotors)]

  def tick(self, motorId):
    if motorId < 1 or motorId > self._numberOfMotors:
      raise Exception("Invalid motor id: " + str(motorId) + " has to be in the range 1 - " + str(self._numberOfMotors))
    self._waitIfNeeded(motorId)
    sequence = self._getSequence(motorId)
    sequence.next()
    self._motorCommunicator.send(motorId, sequence)
    
  def _getSequence(self, motorId):
    return self._sequences[motorId - 1]
      
  def _waitIfNeeded(self, motorId):
    if motorId in self._latestUpdateTime:
      last = self._latestUpdateTime[motorId]
      if last + timedelta(milliseconds=4) > datetime.now():
        print("sleeping")
        time.sleep(0.04)
    self._latestUpdateTime[motorId] = datetime.now()
