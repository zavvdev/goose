# Name: styledText
# Desc: Handle text with stylings
# Args: text (string)
# Return: string

def styledText(text):
  endC = "\033[0m"
  return text + endC

# ----------------------------------------------------