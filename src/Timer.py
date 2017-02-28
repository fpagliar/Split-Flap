import time
import random
from datetime import datetime

class Timer:
  def __init__(self):
    self._registryClockPulseWait = 0.01
    self._registryPublishPulseWait = 0.1 
    self._motorSequenceWait = 0.004
    self._showChunkWait = 60
    self._messageRepetitionWait = 5 * 60
    self._waitForInputRandom = 60
   
  # Shift Registry methods 
   
  def waitRegistryClockPulse(self):
    time.sleep(self._registryClockPulseWait)

  def waitRegistryPublishPulse(self):
    time.sleep(self._registryPublishPulseWait)
    
  def waitBetweenMotorSequences(self):
    time.sleep(self._motorSequenceWait)

  # Message Requester methods

  def waitForInput(self):
    minutes = random.random() * (self._waitForInputRandom - 1) + 1
    time.sleep(60 * minutes)
    
  def waitShowChunk(self):
    time.sleep(self._showChunkWait)
    
  def waitBetweenMessageRepetitions(self):
    time.sleep(self._messageRepetitionWait)
  
  def isAcceptableTimeForMessages(self):
    now = datetime.now()
    return now.hour > self.morningStartTime and now.hour < self.nightStopTime
