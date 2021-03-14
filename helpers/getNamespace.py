import json

def getNamespace(ns):
  data = []
  with open("__locale/namespaces/{}.json".format(ns)) as json_file: 
    data = json.load(json_file) 
  return data