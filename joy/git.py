import os
import subprocess
import time, datetime

def parse_revisions(revtext):
    "Parse revisions text."
    ret = list()
    for line in revtext.split('\n'):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        githash,timestamp = line.split()
        t = time.gmtime(float(timestamp))
        dt = datetime.datetime(*t[:6])
        ret.append((githash, dt))
    return ret;
    
def revisions(filename):
    "Return git revisions for file"
    path = os.path.abspath(filename)
    cmd = "git log --pretty=format:'%%H %%at' --reverse -- %s" % path
    text = subprocess.check_output(cmd, shell=True,
                                   cwd=os.path.dirname(path))
    return text
    
