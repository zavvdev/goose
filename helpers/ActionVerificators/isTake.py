from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces

def isTake(action):
	trimmed = trimSpaces(action)
	s = trimmed.split(" ")
	if len(s) >= 2:
		return s[0] == Act["Take"]
	return False
	pass