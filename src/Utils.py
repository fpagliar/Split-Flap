
def askForConfirmation(message, wait = 0):
 # answer = input(message + " (y/N): ")  # issue with different python versions, input not working on my pi
  answer = raw_input(message + " (y/N): ")
  return answer and (answer[0] == "Y" or answer[0] == "y")

def askForOption(message, dictionary):
  answer = input(message + ": ")
  if answer in dictionary:
    return dictionary.index(answer)
  else:
    print("Invalid input, please try again")
    return askForOption(message, dictionary)
