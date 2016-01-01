#!/usr/bin/env python

import os
from collections import namedtuple

def parse(filenames):
    "Parse the config file names, return configuration as dict"

    try:                from ConfigParser import SafeConfigParser
    except ImportError: from configparser import SafeConfigParser
    cfg = SafeConfigParser()

    cfg.add_section('joy compile')
    cfg.set('joy compile','org_path',os.environ.get('JOY_ORG_PATH',''))
    cfg.add_section('joy render')
    cfg.set('joy render','template_path',os.environ.get('JOY_TEMPLATE_PATH',''))    

    cfg.read(filenames)
    
    dat = dict()
    for secname in cfg.sections():
        sec = dict()
        dat[secname] = sec
        for k,v in cfg.items(secname):
            v = os.path.expandvars(v)
            v = os.path.expanduser(v)
            sec[k] = v

    return dat
