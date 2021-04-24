import os

def getNextPath(curPath, dest, trailingSlash=False):
  slash = "/" if trailingSlash else ""
  path = os.path
  return path.abspath(path.join(curPath, dest)) + slash
