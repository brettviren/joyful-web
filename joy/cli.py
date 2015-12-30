import click
import joy.org, joy.git, joy.render

@click.group()
def cli():
    pass

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
    open(output,'w').write(text)
    return    

@cli.command()
@click.option('-o', '--output', default="/dev/stdout",
              help="Name the output file.")
@click.argument('orgfile')
def revisions(output, orgfile):
    "Get the revisions of an Org file assuming it is manged by Git"
    text = joy.git.revisions(orgfile)
    open(output,'w').write(text)
    return    


@cli.command()
@click.option('-o', '--output', default="/dev/stdout",
              help="Name the output file.")
@click.option('-j', '--json', default=None,
              help="Give a corresponding and previously exported JSON file.")
@click.option('-b', '--body', default=None,
              help="Give a corresponding and previously exported body file.")
@click.option('-r', '--revs', default=None,
              help="Give a corresponding and previously exported git revision file.")
@click.argument('template')
@click.argument('orgfile')
def render(output, json, body, revs, template, orgfile):
    if json:
        json = open(json).read()
    if body:
        body = open(body).read()
    if revs:
        revs = open(revs).read()

    org = joy.org.OrgFile(orgfile, json, body, revs)
    env = joy.render.get_env(orgfile)
    tmplobj = env.get_template(template)
    text = tmplobj.render(**org.params())
    open(output,'w').write(text)
    return

def main():
    cli()

