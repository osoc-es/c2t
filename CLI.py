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


@cli.command()
@click.argument('name')
def dockerhub(name):
    """ Inspect an image from dockerhub """
    os.system(('docker pull '+ name))
    os.system(('docker inspect '+ name))


@cli.command()
@click.argument('name')
def dockerfile(name):
    "Inspect your image from your local dockerfile"
    os.system(("docker build . -t "+name))
    os.system(("docker inspect "+name))


if __name__ == '__main__':
    cli()
