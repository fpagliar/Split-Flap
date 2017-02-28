from queue import Queue

class MessageRequester:
  def __init__(self, timer, feed, logger, display):
    self._timer = timer
    self._feed = feed
    self._logger = logger
    self._display = display
    self._messageQueue = Queue(maxsize=0)
    
  def start(self):
    while True:
      if self._timer.isAcceptableTime():
        self.tick()
      self._timer.waitForInput()
  
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
    for _ in range(5):
      for chunk in chunks:
        self._display.show(chunk)
        self._timer.waitShowChunk()
      self._timer.waitBetweenMessageRepetitions()
    self._messageQueue.task_done()
    
  def chunkinize(self, message):
    # TODO: split the message in chunks, show one chunk at a time with a -
    # return [ message[i:i+chunk_size] for i in range(0, len(message), _display.size()) ]
    # return [ message[i:i+chunk_size]+"-" for i in range(0, len(message), _display.size() - 1) ]
    return message[:self._display.size()]
  
  def _readBatch(self):
    for line in self._feed:
        self._loadLine(line)
    self._feed.truncate(0)
    
  def _loadLine(self, message):
    self._logger.write("READ: " + message)
    self._messageQueue.put(message)
