import time
import calendar

# Name: getTimestamp
# Desc: Get current timestamp
# Args: void
# Return: number

def getTimestamp():
  return calendar.timegm(time.gmtime())

# ----------------------------------------------------