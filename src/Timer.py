import time
import random
from datetime import datetime

# Class used to wait for different time-constraint events
class Timer:
  def __init__(self):
    self._registryClockPulseWait = 0.0000001
    self._registryPublishPulseWait = 0.000001 
    self._motorSequenceWait = 0.00001
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

# from datetime import datetime
# import time
# 
# _registered = {}
# _lastHits = {}
# 
# def register(keyword, seconds):
#   _registered[keyword] = seconds
#   _lastHits[keyword] = datetime.now()
# 
# def waitFor(keyword):
#   if keyword not in _registered:
#     raise Exception("Invalid clock keyword:" + keyword)
# 
#   now = datetime.now()
#   seconds = _registered[keyword]
#   if _lastHits[keyword] + seconds < now:
#     time.sleep(seconds)
#   _lastHits[keyword] = now
