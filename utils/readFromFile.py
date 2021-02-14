import json

def readFromFile(pathToFile):
  try:
    data = []
    with open(pathToFile) as json_file: 
      data = json.load(json_file) 
    return data
  except:
    return False