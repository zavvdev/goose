from utils.styledText import styledText
from constants.textStyles import textStyles
from modules.Namespace import Namespace
from utils.getHelp import getHelp

ns = Namespace()

class Message:
  def default(self, text):
    print(text)

  def welcome(self):
    welcomeMessage = ns.common["welcome_message"]
    style = textStyles["Bold"] + textStyles["White"]
    print(styledText(style + welcomeMessage))

  def error(self, text):
    print(styledText(textStyles["Red"] + text))

  def info(self, text):
    print(styledText(textStyles["Yellow"] + text))

  def success(self, text):
    print(styledText(textStyles["Green"] + text))

  def suspend(self, text):
    print(styledText(textStyles["Violet"] + text))

  def serverResponse(self, text):
    print(ns.common["server_says"], text)

  def help(self):
    print(getHelp())