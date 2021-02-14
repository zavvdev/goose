import json

def writeToFile(data, pathToFile):
  try:
    with open(pathToFile, "w", encoding = "utf-8") as f:
      json.dump(data, f, ensure_ascii = False, indent = 2)
    return True
  except:
    return False