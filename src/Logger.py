
from Configuration import defaultSystemConfiguration, Keywords

_config = defaultSystemConfiguration()

def log(tag, invoker, message):
  if _config.get(Keywords.DEBUG_MODE) and invoker in _config.get(Keywords.LOGGER_TAGS):
    print(invoker + "> " + message)