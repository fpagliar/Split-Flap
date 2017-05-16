
from Configuration import SystemConfiguration

_config = SystemConfiguration()

def log(invoker, message):
  if _config.isDebugMode() and _config.shouldLog(invoker.__class__.__name__):
    print(invoker.logId() + "> " + message)