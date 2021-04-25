import os

# Name: getNextPath
# Desc: Form absolute path
# Args: curPath (string), dest (string), trailingSlash (boolean)
# Return: string

def getNextPath(curPath, dest, trailingSlash=False):
  slash = "/" if trailingSlash else ""
  path = os.path
  return path.abspath(path.join(curPath, dest)) + slash

# ----------------------------------------------------