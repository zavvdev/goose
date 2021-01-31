from ftplib import FTP
from goose.utils.Menu import Menu

greeting_menu = ["Upload", "Download", "Disconnect"]
greeting_menu = Menu(greeting_menu)

def rush(ftp_adress):
  print("Rushing " + ftp_adress + "...")
  
  try:
    ftp = FTP(ftp_adress)
    username = input("Enter username: ")
    password = input("Enter password: ")
    print(ftp.login(user="dlpuser", passwd="rNrKYTX9g7z3RgJRmxWuGHbeu"))
    # data = ftp.retrlines('LIST')
    custom_text = [
      "Successfuly connected to {}".format(ftp_adress),
      "{adress}@{user}".format(adress=ftp_adress, user="dlpuser"), 
      "Choose what you want to do next:",
    ]
    greeting_menu.print_with(custom_text)

    chosed_item = greeting_menu.get_selected_item()
    print(chosed_item)
  except:
    print("Error!")
  pass