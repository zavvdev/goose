from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces

def isDrop(action):
	trimmed = trimSpaces(action)
	s = trimmed.split(" ")
	if len(s) >= 2:
		return s[0] == Act["Drop"]
	return False
	pass