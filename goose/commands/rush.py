from ftplib import FTP
from goose.utils.Menu import Menu

def rush(ftp_adress):
  print("Rushing " + ftp_adress + "...")
  _Menu = Menu(["Home", "Desktop", "Documents", "Exit"])
  try:
    ftp = FTP(ftp_adress)
    print(ftp.login())
    data = ftp.retrlines('LIST')
    print(data)
    _Menu.print()
  except:
    username = input("Enter username: ")
    password = input("Enter password: ")
    print(ftp.login(user=username, passwd = password))
    data = ftp.retrlines('LIST')
    print(data)
    _Menu.print()
  pass