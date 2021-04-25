import json
from constants.nsAccessors import nsAccessors

# Name: Namespace
# Desc: Provide interface for accessing application namespaces
# Inherits: None
# Methods: 
#   - __getNamespace (get specific namespace)
# Fields:
#   - common (common namespaces)
#   - rush (rush action namespaces)
#   - jump (jump action namespaces)
#   - cd (cd action namespaces)
#   - mkdir (mkdir action namespaces)
#   - delete (delete action namespaces)
#   - put (put action namespaces)
#   - take (take action namespaces)
#   - clear (clear action namespaces)
#   - ls (ls action namespaces)
#   - status (status action namespaces)

class Namespace:
  def __init__(self):
    self.common = self.__getNamespace(nsAccessors["Common"])
    self.rush = self.__getNamespace(nsAccessors["Rush"])
    self.jump = self.__getNamespace(nsAccessors["Jump"])
    self.cd = self.__getNamespace(nsAccessors["Cd"])
    self.mkdir = self.__getNamespace(nsAccessors["Mkdir"])
    self.delete = self.__getNamespace(nsAccessors["Delete"])
    self.put = self.__getNamespace(nsAccessors["Put"])
    self.take = self.__getNamespace(nsAccessors["Take"])
    self.clear = self.__getNamespace(nsAccessors["Clear"])
    self.ls = self.__getNamespace(nsAccessors["Ls"])
    self.status = self.__getNamespace(nsAccessors["Status"])

  # ----------------------------------------------------

  # Name: __getNamespace
  # Desc: Get specific namespace
  # Args: accessor (string<Key of Actions>)
  # Return: Dictionary

  def __getNamespace(self, accessor):
    data = []
    with open("namespaces/{}.json".format(accessor)) as json_file: 
      data = json.load(json_file) 
    return data

  # ----------------------------------------------------