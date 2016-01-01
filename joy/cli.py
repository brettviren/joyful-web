import os.path as osp
import click
import json
import joy.config, joy.io, joy.org, joy.git


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
    org_path = cfg['joy compile']['org_path']

    doc = dict(
        orgtext = joy.io.load(orgfile),
        orghtml = joy.org.convert(orgfile, 'body'),
        orgtree = json.loads(joy.org.convert(orgfile, 'json')),
        revs = joy.git.parse_revisions(joy.git.revisions(orgfile)),
    )

    # locate source file in various ways
    root = joy.io.subdir_in_path(orgfile, org_path)
    doc['orgroot'] = root
    doc['orgabsroot'] = osp.abspath(root)
    doc['orgsubdir'] = osp.dirname(orgfile)
    doc['orgfilename'] = osp.basename(orgfile)
    doc['orgabsfilepath'] = osp.abspath(osp.join(root,orgfile))

    doc['meta'] = joy.org.summarize(doc['orgtree'])

    joy.io.save_json(output, doc)
    return    


@cli.command()
@click.option('-o', '--output', default="/dev/stdout",
              help="Name the output file.")
@click.option('-t', '--template-path', envvar="JOY_TEMPLATE_PATH",
              multiple=True, type=click.Path(),
              help="Set the path to find templates.")
@click.argument('template')
@click.argument('filenames',nargs=-1)
@click.pass_context
def render(ctx, output, template_path, template, filenames):
    "Render the data in JSON files with the template"

    cfg = ctx.obj['cfg']

    # joy render parameters
    if template_path:
        cfg['joy render']['template_path'] = template_path
    template_path = cfg['joy render']['template_path']

    docs = list()
    for fname in filenames:
        doc = joy.io.load_json(fname)
        docs.append(doc)

    tcfg = cfg.get('global',dict())
    tsec = 'template %s' % template
    tcfg.update(cfg.get(tsec, dict()))

    env = joy.render.get_env(template_path)
    tmplobj = env.get_template(template)
    text = tmplobj.render(doc = docs, cfg=tcfg, **docs[0])
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
@click.pass_context
def export(list_formats, format, output, orgfile):
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

