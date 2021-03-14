from helpers.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors

commonNS = getNamespace(nsAccessors["Common"])

def printServerResponseMsg(msg):
  print(commonNS["server_says"], msg)
  pass