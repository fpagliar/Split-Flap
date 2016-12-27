def askForConfirmation(message):
  answer = input(message + " (Y/N): ")
  if answer and answer[0] == "Y":
    return True
  elif answer and answer[0] == "N":
    return False
  else:
    print("Invalid input, please try again")
    return askForConfirmation(message)