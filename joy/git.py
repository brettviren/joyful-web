import os
import subprocess
import time, datetime

def parse_revisions(revtext):
    "Parse revisions text."
    revs = list()
    for line in revtext.split('\n'):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        githash,timestamp = line.split()
        revs.append((githash, float(timestamp)))

    return revs

    
def revisions(filename):
    "Return git revisions for file"
    path = os.path.abspath(filename)
    cmd = "git log --pretty=format:'%%H %%at' --reverse -- %s" % path
    text = subprocess.check_output(cmd, shell=True,
                                   cwd=os.path.dirname(path))
    return text
    
