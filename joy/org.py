#!/usr/bin/env python
'''
Joyful interface to Org.
'''

import joy.git
import os, os.path as osp
import json
import tempfile
import subprocess
import time
import datetime

emacs = "/usr/bin/emacs"
pkgdir = os.path.dirname(__file__)

def convert(orgfile, format="body"):
    """Call Emacs to convert orgfile to format.
    
    For each format there must be a org2<format>.el file in the joy
    Python package directory containing a function named org2<format>
    which is called like (org2<format> src dst).

    """
    _, outfile = tempfile.mkstemp('.'+format, prefix='joyorgconvert')

    elfile = os.path.join(pkgdir, 'org2%s.el'%format)
    cmd = [emacs, '-Q', '--batch', '-l', elfile, '--eval']
    cmd += ["(org2%s \"%s\" \"%s\")" % (format, orgfile, outfile)]
    stderr = subprocess.STDOUT
    subprocess.check_output(cmd, stderr=stderr)
    text = open(outfile).read()
    os.remove(outfile)
    return text

def document_keywords(j):
    'Interpret loaded Org JSON structure and return main section keywords'
    if j[0] != "org-data": return
    section = j[2]
    if section[0] != "section": return
    ret = dict()
    for part in section[2:]:
        if part[0] != "keyword":
            continue
        kwrec = part[1]
        ret[kwrec['key'].lower()] = kwrec['value']
    return ret;

def headline_structure(j):
    'Interpret loaded Org JSON structure and return headline structure'
    if j[0] != "org-data": return

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

    return headlines(j[2:])


class OrgFile(object):
    'Collection of all there is to know about an Org file'

    def __init__(self, orgfile, jsontext=None, bodytext=None, revstext=None):
        'Create an OrgFile object'
        self.orgpath = osp.abspath(orgfile)
        self.orgfile = osp.basename(orgfile)
        self.orgtext = open(self.orgpath).read()

        # get JSON representation of Org document
        if not jsontext:
            jsontext = convert(self.orgpath, "json")
        self.orgtree = json.loads(jsontext)
        self.meta = document_keywords(self.orgtree)
        self.headlines = headline_structure(self.orgtree)

        if not revstext:
            revstext = joy.git.revisions(self.orgpath)
        if revstext:
            revs = joy.git.parse_revisions(revstext)
            self.created = revs[0][1]
            self.revised = revs[-1][1]
        else:                   # make up something based on file stat
            s = os.stat(self.orgpath)
            ct = time.gmtime(s.st_ctime)
            self.created = datetime.datetime(*ct[:6])
            mt = time.gmtime(s.st_mtime)
            self.revised = datetime.datetime(*mt[:6])

        if not bodytext:
            bodytext = convert(self.orgpath, "body")
        self.body = bodytext
        return
    def params(self):
        return self.__dict__
