from utils.styledText import styledText
from constants.textStyles import textStyles
from modules.Namespace import Namespace
from utils.getHelp import getHelp

ns = Namespace()

# Name: Message
# Desc: Provide interface for using application messages with custom styling
# Methods: 
#   - default (print default message)
#   - welcome (print welcome app message)
#   - error (print error message)
#   - info (print info message)
#   - success (print success message)
#   - help (print help message)

class Message:

  # Name: default
  # Desc: Print default message
  # Args: text (string)
  # Return: void

  def default(self, text):
    print(text)

  # ----------------------------------------------------

  # Name: welcome
  # Desc: Print welcome app message
  # Args: void
  # Return: void

  def welcome(self):
    welcomeMessage = ns.common["welcome_message"]
    style = textStyles["Bold"] + textStyles["White"]
    print(styledText(style + welcomeMessage))

  # ----------------------------------------------------

  # Name: error
  # Desc: Print error message
  # Args: text (string)
  # Return: void

  def error(self, text):
    print(styledText(textStyles["Red"] + text))

  # ----------------------------------------------------

  # Name: info
  # Desc: Print info message
  # Args: text (string)
  # Return: void

  def info(self, text):
    print(styledText(textStyles["Yellow"] + text))

  # ----------------------------------------------------

  # Name: success
  # Desc: Print success message
  # Args: text (string)
  # Return: void

  def success(self, text):
    print(styledText(textStyles["Green"] + text))

  # ----------------------------------------------------

  # Name: help
  # Desc: Print help message
  # Args: void
  # Return: void

  def help(self):
    print(getHelp())

  # ----------------------------------------------------