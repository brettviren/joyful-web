import os.path as osp
import click
import json
import joy.config, joy.io, joy.org, joy.git, joy.render
import importlib

@click.group()
@click.option('-c', '--config', 
              multiple=True, type=click.Path(),
              help="Set a joyful configuration file.")
@click.pass_context
def cli(ctx, config):
    ctx.obj['cfg'] = joy.config.parse(config)
    return

@cli.command()
@click.pass_context
def dump(ctx):
    print ctx.obj['cfg']


@cli.command()
@click.option('-o', '--output',default="/dev/stdout",
              help="Name the compiled output JSON file.")
@click.option('--org-path', 
              multiple=True, type=click.Path(),
              help="Path to top of org sources.")
@click.argument('orgfile')
@click.pass_context
def compile(ctx, output, org_path, orgfile):
    "Compile the ORG file to the intermediate JSON representation"

    cfg = ctx.obj['cfg']

    # joy compile parameters
    if org_path:
        cfg['joy compile']['org_path'] = org_path
    org_path = cfg['joy compile']['org_path'].split(':')

    # fixme: converting to HTML here as "body" is a biased asymmetry
    # in policy.  How can joy be used to drive Emacs for other
    # document types?
    doc = dict(
        text = joy.io.load(orgfile),
        plain = joy.org.convert(orgfile, 'plain'), 
        body = joy.org.convert(orgfile, 'body'), 
        tree = json.loads(joy.org.convert(orgfile, 'json')),
        revs = joy.git.parse_revisions(joy.git.revisions(orgfile)),
    )

    # locate source file in various ways
    fullpath = osp.abspath(orgfile)
    root = joy.io.subdir_in_path(orgfile, org_path)
    root = osp.abspath(root)
    doc['root'] = root
    relpath = fullpath[len(root)+1:]
    doc['path'] = osp.dirname(relpath)
    doc['name'] = osp.splitext(osp.basename(relpath))[0]

    print 'DOC:', doc['root'],doc['path'],doc['name'],relpath

    joy.io.save_json(output, doc)
    return    


@cli.command()
@click.option('-o', '--output', default="/dev/stdout",
              help="Name the output file.")
@click.option('-t', '--template-path', 
              multiple=True, type=click.Path(),
              help="Set the path to find templates.")
@click.argument('renderer')
@click.argument('filenames',nargs=-1)
@click.pass_context
def render(ctx, output, template_path, renderer, filenames):
    "Render the data in JSON files with the template"

    cfg = ctx.obj['cfg']

    # joy render parameters
    if template_path:
        cfg['joy render']['template_path'] = template_path
    template_path = cfg['joy render']['template_path']

    # build render config
    rcfg = cfg.get('global', dict())
    rsec = 'render %s' % renderer
    rcfg.update(cfg[rsec])
    
    # load previously compiled org structures
    docs = list()
    for fname in filenames:
        doc = joy.io.load_json(fname)
        docs.append(doc)

    # call processors
    dat = dict(org = docs)
    for pname in rcfg.get('processors','').split(','):
        pname = pname.strip()
        if not pname: continue
        print 'Running processor "%s"' % pname
        psec = 'processor %s' % pname
        pcfg = cfg.get('global', dict())
        pcfg.update(cfg[psec])
        modmethname = pcfg['method']
        modname, methname = modmethname.rsplit('.',1)
        mod = importlib.import_module(modname)
        meth = mod.__dict__[methname]
        res = meth(dat, **pcfg)
        dat[pname] = res
        
    # pass any user parameters to template
    dat['cfg'] = rcfg

    template = rcfg['template']
    env = joy.render.get_env(template_path)
    tmplobj = env.get_template(template)
    text = tmplobj.render(**dat)
    joy.io.save(output, text)
    return


@cli.command('list-formats')
def list_formats():
    click.echo(' '.join(joy.org.supported_formats()))

@cli.command()
@click.option('-f','--format',default=None,
              help="Export format.")
@click.option('-o', '--output',default="/dev/stdout",
              help="Name the output file.")
@click.argument('orgfile')
def export(format, output, orgfile):
    "Export a single Org file to a supported output format"
    if not format:
        dot = output.rfind('.')+1
        if not dot: raise RuntimeError,'Can not guess format from output file name.'
        format = output[dot:]

    text = joy.org.convert(orgfile, format)
    joy.io.save(output, text)
    return    



def main():
    cli(obj={})

