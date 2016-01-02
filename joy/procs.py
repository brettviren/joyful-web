import os
import joy.org
import datetime, time

from joy.util import seconds2datetime

def meta(dat, **kwds):
    res = []
    for org in dat['org']:
        summary = joy.org.summarize(org['tree'])

        revs = org['revs']
        if revs:
            ct = revs[0][1]
            mt = revs[-1][1]
        else:                   # make up something based on file stat
            s = os.stat(os.path.join(org['root'], org['path'], org['name'] + '.org'))
            ct = s.st_ctime
            mt = s.st_mtime

        summary['created'] = seconds2datetime(ct)
        summary['revised'] = seconds2datetime(mt)
        res.append(summary)
    return res
