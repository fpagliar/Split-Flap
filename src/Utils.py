import signal

def askForConfirmation(message, timeout = False):
  if timeout:
      answer = _getTimedInput(message, 1)
  else:
      answer = input(message + " (y/N): ")
  return answer and (answer[0] == "Y" or answer[0] == "y")
  
def askForOption(message, dictionary):
  answer = input(message + ": ")
  if answer in dictionary:
    return dictionary.index(answer)
  else:
    print("Invalid input, please try again")
    return askForOption(message, dictionary)


def _interrupted(signum, frame):
    "called when read times out"
    pass

def _getTimedInput(message, timeout):
    signal.signal(signal.SIGALRM, _interrupted)
    # set alarm
    signal.alarm(timeout)
    value = _getInput(message)
    # disable the alarm after success
    signal.alarm(0)
    return value

def _getInput(message):
    try:
        return input(message + " (Y/n): ")
    except:
        # timeout
        return False
