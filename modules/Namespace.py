import json
from constants.nsAccessors import nsAccessors

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

  def __getNamespace(self, accessor):
    data = []
    with open("namespaces/{}.json".format(accessor)) as json_file: 
      data = json.load(json_file) 
    return data