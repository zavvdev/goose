import json
from constants.nsAccessors import nsAccessors

# Name: Namespace
# Desc: Provide interface for accessing application namespaces
# Methods: 
#   - __getNamespace (get specific namespace)
# Fields:
#   - common (common namespaces)
#   - interact (Interact module namespaces)
#   - errors (namespaces for error messages)
#   - infos (namespaces for info messages)
#   - suspends (namespaces for suspend messages)

class Namespace:
  def __init__(self):
    self.common = self.__getNamespace(nsAccessors["Common"])
    self.interact = self.__getNamespace(nsAccessors["Interact"])
    self.errors = self.__getNamespace(nsAccessors["Errors"])
    self.infos = self.__getNamespace(nsAccessors["Infos"])
    self.suspends = self.__getNamespace(nsAccessors["Suspends"])

  # Name: __getNamespace
  # Desc: Get specific namespace
  # Args: accessor (string<Key of actions>)
  # Return: Dictionary

  def __getNamespace(self, accessor):
    data = []
    with open("namespaces/{}.json".format(accessor)) as json_file: 
      data = json.load(json_file) 
    return data

  # ----------------------------------------------------