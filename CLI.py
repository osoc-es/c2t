import click
import os 


@click.group()
def cli():
    '''This is a tool for your docker containers.'''
    pass


@cli.command()
@click.argument('name')
def image(name):
    """ Inspect your image from its name or ID """
    os.system(('docker inspect '+ name))
    os.system(('syft '+name+' -o cyclonedx-json'))

@cli.command()
@click.argument('name')
def dockerhub(name):
    """ Inspect an image from dockerhub """
    os.system(('docker pull '+ name))
    os.system(('docker inspect '+ name))
    os.system(('syft '+name+' -o cyclonedx-json'))

@cli.command()
@click.argument('name')
def dockerfile(name):
    "Inspect your image from your local dockerfile. The name must be between 2 and 255 letters."
    os.system(("docker build . -t "+name))
    os.system(("docker inspect "+name))
    os.system(('syft '+name+' -o cyclonedx-json'))


if __name__ == '__main__':
    cli()
