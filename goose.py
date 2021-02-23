from ftplib import FTP

#--------# Settings #--------#

ftp = None

class C:
  VIOLET = '\033[95m'
  BLUE = '\033[94m'
  CYAN = '\033[96m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

#--------# Commangs verificators #--------#

def isExit(i):
  return i == "exit" or i == "x"
  pass

def isHelp(i):
  return i == "help" or i == "h"
  pass

def isRush(i):
  s = i.split(" ")
  rushHere = s[0] == "rush"
  hAccessorHere = len(s) == 2
  uAccessorHere = len(s) == 4 and s[2] == "as"
  pAccessorHere = len(s) == 6 and s[2] == "as" and s[4] == "with"
  return rushHere and (hAccessorHere or uAccessorHere or pAccessorHere)
  pass

#--------# Utils #--------#

def login(d):
  try:
    global ftp
    ftp = FTP(d["h"])
    ftp.login(user=d["u"], passwd=d["p"])
    return True
  except:
    return False

#--------# Actions #--------#

def help():
  pass

def rush(i):
  s = i.split(" ")
  l = len(s)
  d = {}

  print(C.VIOLET + "Rushing to " + s[1] + ".." + C.ENDC)

  if l == 2:
    d = { "h": s[1], "u": "", "p": ""}
  elif l == 4:
    d = { "h": s[1], "u": s[3], "p": "" }
  else:
    d = { "h": s[1], "u": s[3], "p": s[5] }

  if login(d):
    print(C.GREEN + "Connected successful!" + C.ENDC)
    ftp.retrlines("LIST") 
  else:
    print("Error")
  pass

#--------# Main #--------#

def goose():
  print(C.BOLD + "\nGoose v0.0.1. FTP cli tool." + C.ENDC)

  while True:
    i = input(C.CYAN + C.BOLD + "goose~>: " + C.ENDC)

    if isExit(i):
      break
    elif isHelp(i):
      print("Help will be here")
    elif isRush(i):
      rush(i)
    else:
      print(C.YELLOW + "Goose dont understand u. Type \"help\" or \"h\" for list of commands" + C.ENDC)
  pass

goose()