def getUserInput(fields):
  result = {}
  for field in fields:
    userInput = input(field + ": ")
    result[field] = userInput
  return result
  pass
