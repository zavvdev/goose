import subprocess

def execCmd(command):
  process = subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
  stdout = process.communicate()[0].strip()
  return stdout.decode("utf-8")