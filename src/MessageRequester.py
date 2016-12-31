from queue import Queue
from datetime import datetime
import time
import random

class MessageRequester:
  def __init__(self, feed, logger, display):
    self._feed = feed
    self._logger = logger
    self._display = display
    self._messageQueue = Queue(maxsize=0)
    
  def start(self):
    while True:
      if self.isAcceptableTime():
        self.tick()
      minutes = random.random() * 59 + 1
      time.sleep(60 * minutes)
  
  def isAcceptableTime(self):
    now = datetime.now()
    return now.hour > 10 and now.hour < 23

  def tick(self):
    if self._messageQueue.empty():
      self._readBatch()
    if not self._messageQueue.empty():
      self._processMessage()
      
  def _processMessage(self):
    message = self._messageQueue.get()
    
    with open(self._logger, "a") as myfile:
      myfile.write("SHOW: " + message)

    chunks = self.chunkinize(message)
    for _ in range(0, 5):
      for chunk in chunks:
        self._display.show(chunk)
        time.sleep(60)
      time.sleep(60 * 5)

    self._messageQueue.task_done()
    
  def chunkinize(self, message):
    # TODO: split the message in chunks, show one chunk at a time with a -
    # return [ message[i:i+chunk_size] for i in range(0, len(message), _display.size()) ]
    # return [ message[i:i+chunk_size]+"-" for i in range(0, len(message), _display.size() - 1) ]
    return message[:self._display.size()]
  
  def _readBatch(self):
#     with open(self._feed, 'rw+') as file:
    for line in self._feed:
        self._loadLine(line)
    self._feed.truncate(0)
    
  def _loadLine(self, message):
#     with open(self._logger, "a") as myfile:
    self._logger.write("READ: " + message)
    self._messageQueue.put(message)
