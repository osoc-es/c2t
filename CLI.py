import click
import os 
import syft_parser 

@click.group()
def cli():
    '''This is a tool for your docker containers.'''
    pass


@cli.command()
@click.argument('name')
@click.argument('output')
def image(name, output):
    """ Inspect your image from its name or ID """
    os.system(('docker inspect '+ name))
    syft = os.popen(('syft '+name+' -o cyclonedx-json')).read()
    print(syft)
    syft_parser.parse_data(syft, output+'.json')


@cli.command()
@click.argument('name')
@click.argument('output')
def dockerhub(name, output):
    """ Inspect an image from dockerhub """
    os.system(('docker pull '+ name))
    os.system(('docker inspect '+ name))
    syft = os.popen(('syft '+name+' -o cyclonedx-json')).read()
    print(syft)
    syft_parser.parse_data(syft, output+'.json')



@cli.command()
@click.argument('name')
@click.argument('output')
def dockerfile(name, output):
    "Inspect your image from your local dockerfile. The name must be between 2 and 255 letters."
    os.system(("docker build . -t "+name))
    os.system(("docker inspect "+name))
    syft = os.popen(('syft '+name+' -o cyclonedx-json')).read()
    print(syft)
    syft_parser.parse_data(syft, output+'.json')


if __name__ == '__main__':
    cli()
