from ftplib import FTP

def rush(ftp_adress):
  print("Rushing " + ftp_adress + "...")
  try:
    ftp = FTP(ftp_adress)
    print(ftp.login())
    data = ftp.retrlines('LIST')
    print(data)
  except:
    username = input("Enter username: ")
    password = input("Enter password: ")
    print(ftp.login(user=username, passwd = password))
    data = ftp.retrlines('LIST')
    print(data)
  pass