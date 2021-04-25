import subprocess

# Name: execCmd
# Desc: Execute Linux terminal command
# Args: command (string)
# Return: any

def execCmd(command):
  try:
    process = subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
    stdout = process.communicate()[0].strip()
    return stdout.decode("utf-8")
  except:
    return False

# ----------------------------------------------------