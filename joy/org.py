#!/usr/bin/env python
'''
Joyful interface to Org.
'''

import os
import sys
import shutil
import tempfile
import subprocess

emacs = "/usr/bin/emacs"
pkgdir = os.path.dirname(__file__)

def body(orgfile):
    "Export the Org file and return the body of the resulting HTML"

    _, htmlfile = tempfile.mkstemp('.html', prefix='joyorgbody')

    elisp = os.path.join(pkgdir, 'org2body.el')
    cmd = [emacs, '-Q', '--batch', '-l', elisp, '--eval']
    cmd += ["(org2body \"%s\" \"%s\")" % (orgfile, htmlfile)]
    stderr = subprocess.STDOUT
    subprocess.check_output(cmd, stderr=stderr)
    html = open(htmlfile).read()
    os.remove(htmlfile)
    return html


