def askForConfirmation(message):
  answer = input(message + " (Y/N): ")
  if answer and answer[0] == "Y":
    return True
  elif answer and answer[0] == "N":
    return False
  else:
    print("Invalid input, please try again")
    return askForConfirmation(message)
  
def askForOption(message, dictionary):
  answer = input(message + ": ")
  if answer in dictionary:
    return dictionary.index(answer)
  else:
    print("Invalid input, please try again")
    return askForOption(message, dictionary)
  