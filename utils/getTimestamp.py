import time
import calendar

def getTimestamp():
  return calendar.timegm(time.gmtime())