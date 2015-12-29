import click
import joy.org

@click.group()
def cli():
    pass

@cli.command()
@click.option('-o','--output',default="/dev/stdout",help="Name the output file.")
@click.argument('orgfile')
def body(output, orgfile):
    html = joy.org.body(orgfile)
    open(orgfile,'w').write(html)
    return    



def main():
    cli()

