

_isLogging = [False]

def debug():
  _isLogging[0] = True

def log(message):
  if _isLogging[0]:
    print(message)