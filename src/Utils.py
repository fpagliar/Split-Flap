def askForConfirmation(message):
  answer = input(message + " (y/N): ")
  if answer and answer[0] == "Y":
    return True
  else:
    return False
  
def askForOption(message, dictionary):
  answer = input(message + ": ")
  if answer in dictionary:
    return dictionary.index(answer)
  else:
    print("Invalid input, please try again")
    return askForOption(message, dictionary)
  