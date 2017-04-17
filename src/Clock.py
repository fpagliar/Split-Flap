from datetime import datetime
import time

_registered = {}
_lastHits = {}

def register(keyword, seconds):
  _registered[keyword] = seconds
  _lastHits[keyword] = datetime.now()

def waitFor(keyword):
  if keyword not in _registered:
    raise Exception("Invalid clock keyword:" + keyword)

  now = datetime.now()
  seconds = _registered[keyword]
  if _lastHits[keyword] + seconds < now:
    time.sleep(seconds)
  _lastHits[keyword] = now
