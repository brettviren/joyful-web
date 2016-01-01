#!/usr/bin/env python
'''
Wrap I/O functions.
'''

import os.path as osp
import json

def load(filename):
    "Read file as text, return text"
    return open(filename).read()

def save(filename, text):
    "Write text to file"
    open(filename,"w").write(text)
    

def load_json(filename):
    "Read file as JSON, return data tructure"
    return json.loads(load(filename))

def save_json(filename, dat):
    "Save data structure to json file"
    text = json.dumps(dat, indent=2)
    save(filename, text)

def subdir_in_path(filepath, path):
    "Return the first entry of <path> which contains filepath"
    if type(path) == type(""):
        path = path.split(":")
    for maybe in path:
        if osp.exists(osp.join(maybe, filepath)):
            return maybe
    return None
