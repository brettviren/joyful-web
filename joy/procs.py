import os
import joy.org
import datetime, time

def meta(dat, **kwds):
    res = []
    for org in dat['org']:
        meta = joy.org.summarize(org['tree'])

        revs = org['revs']
        if revs:
            ct = time.gmtime(revs[0][1])
            meta['created'] = datetime.datetime(*ct[:6])
            rt = time.gmtime(revs[-1][1])
            meta['revised'] = datetime.datetime(*rt[:6])
        else:                   # make up something based on file stat
            s = os.stat(os.path.join(org['root'], org['path'], org['name'] + '.org'))
            ct = time.gmtime(s.st_ctime)
            meta['created'] = datetime.datetime(*ct[:6])
            mt = time.gmtime(s.st_mtime)
            meta['revised'] = datetime.datetime(*mt[:6])


        res.append(meta)
    return res
