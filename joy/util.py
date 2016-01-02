
import time, datetime

def seconds2datetime(sec):
    t = time.gmtime(float(sec))
    return datetime.datetime(*t[:6])
    
