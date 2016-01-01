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
        #t = time.gmtime(float(timestamp))
        #dt = datetime.datetime(*t[:6])
        #ret.append((githash, dt))
        ret.append((githash, float(timestamp)))
    return ret;
    
def revisions(filename):
    "Return git revisions for file"
    path = os.path.abspath(filename)
    cmd = "git log --pretty=format:'%%H %%at' --reverse -- %s" % path
    text = subprocess.check_output(cmd, shell=True,
                                   cwd=os.path.dirname(path))
    return text
    
        # if not revstext:
        #     revstext = joy.git.revisions(self.orgpath)
        # if revstext:
        #     revs = joy.git.parse_revisions(revstext)
        #     self.created = revs[0][1]
        #     self.revised = revs[-1][1]
        # else:                   # make up something based on file stat
        #     s = os.stat(self.orgpath)
        #     ct = time.gmtime(s.st_ctime)
        #     self.created = datetime.datetime(*ct[:6])
        #     mt = time.gmtime(s.st_mtime)
        #     self.revised = datetime.datetime(*mt[:6])

