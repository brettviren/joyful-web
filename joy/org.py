#!/usr/bin/env python
'''
Joyful interface to Org.
'''

import joy.git
import os, os.path as osp
import shutil
import json
import tempfile
import subprocess
import time
import datetime
import pytz

# fixme: let this be set by user/config
emacs = "/usr/bin/emacs"
pkgdir = os.path.dirname(__file__)

def convert(orgfile, format="body"):
    """Call Emacs to convert orgfile to format.

    Warning: emacs is run in-place in the directory containing the
    orgfile.  If exporting the Org file has any side-effect file
    production these files are not cleaned up.
    
    For each format there must be a org2<format>.el file in the joy
    Python package directory containing a function named org2<format>
    which is called like (org2<format> src dst).

    """
    _, outfile = tempfile.mkstemp('.'+format, prefix='joyorgconvert')
    orgfile = osp.abspath(orgfile)
    orgdir = osp.dirname(orgfile)

    elfile = os.path.join(pkgdir, 'org2%s.el'%format)
    cmd = [emacs, '-Q', '--batch', '-l', elfile, '--eval']
    cmd += ["(org2%s \"%s\" \"%s\")" % (format, orgfile, outfile)]
    print 'Calling from %s: %s' % (orgdir, ' '.join(cmd))
    stderr = subprocess.STDOUT
    subprocess.check_output(cmd, stderr=stderr, cwd=orgdir)
    text = open(outfile).read()
    os.remove(outfile)
    return text

def summarize(orgtree, **kwds):
    "Return a dictionary summarizing the orgtree"
    kwds = document_keywords(orgtree)
    kwds['tags'] = kwds.get('tags','').split(',')
    kwds['headlines'] = headline_structure(orgtree)
    ts = kwds.get('date',None)
    if ts:                      # this is painful
        ts = ts.strip()
        if ts.startswith('['):
            ts = ts[1:-1]
        tt = time.strptime(ts,'%Y-%m-%d %a %H:%M')
        dt = datetime.datetime(*tt[:6])
        dt = dt.replace(tzinfo = pytz.timezone('US/Eastern'))
        kwds['timestamp'] = dt

    return kwds


def document_keywords(orgtree):
    'Interpret loaded Org JSON structure and return main section keywords'
    if len(orgtree) < 3:
        raise RuntimeError, 'truncated org-tree %s' % str(orgtree)

    if orgtree[0] != "org-data":
        raise RuntimeError, 'not an org-tree, got "%s"' % orgtree[0]

    section = orgtree[2]
    if section[0] != "section":
        return dict()           # no leading section

    ret = dict()
    for part in section[2:]:
        if part[0] != "keyword":
            continue
        kwrec = part[1]
        ret[kwrec['key'].lower()] = kwrec['value']
    return ret;

def headline_structure(orgtree):
    'Interpret loaded Org JSON structure and return headline structure'
    if orgtree[0] != "org-data": return

    def headlines(entries, root=None):
        root = root or []
        count = 0;
        ret = list()
        for ent in entries:
            if type(ent) != list:
                print 'What is this?', str(ent)
                continue
            if not ent: continue
            if ent[0] != "headline": continue
            count += 1
            kwds = ent[1]
            thisroot = root + [count]
            ret.append((thisroot, kwds['raw-value']))
            ret += headlines(ent[2:], thisroot)
        return ret;

    return headlines(orgtree[2:])

def supported_formats():
    fmts = list()
    for fname in os.listdir(pkgdir):
        if not fname.endswith('.el'): continue
        if not fname.startswith('org2'): continue
        fmts.append(fname[4:-3])
    return fmts

