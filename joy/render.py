import os.path as osp

def get_template_dirs(path, top="/"):
    "Return all template directories along the path"
    path = osp.abspath(path)
    if osp.isfile(path):
        path = osp.dirname(path)
    templates = []
    while path:
        maybe = osp.join(path, 'templates')
        if osp.isdir(maybe):
            templates.append(maybe)
        if path == top:
            break;
        path = osp.dirname(path)
        if path == "/":
            break
    templates.reverse()
    return templates

def get_env(template_path):
    "Return the template environment for a given source file"
    if type(template_path) == type(""):
        template_path = template_path.split(":")
    from jinja2 import Environment, FileSystemLoader
    return Environment(loader=FileSystemLoader(template_path))



