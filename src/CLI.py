import click
import os 
import syft_parser as syft_parser 
import morph_kgc

def get_graph(name):
    os.system(('docker inspect '+ name+' > ../data/inspect1.json'))
    syft = os.popen(('syft '+name+' -o cyclonedx-json')).read()
    syft_parser.parse_data(syft, '../data/result1.json')
    g = morph_kgc.materialize('../config.ini')
    g.serialize(destination="grafo.nt", format="ntriples")

@click.group()
def cli():
    '''This is a tool for your docker containers.'''
    pass


@cli.command()
@click.argument('name')
def image(name):
    """ Inspect your image from its name or ID """
    get_graph(name)


@cli.command()
@click.argument('name')
def dockerhub(name):
    """ Inspect an image from dockerhub """
    os.system(('docker pull '+ name))
    os.system(('docker inspect '+ name+' > inspect.json'))
    syft = os.popen(('syft '+name+' -o cyclonedx-json')).read()
    syft_parser.parse_data(syft, 'result.json')
    


@cli.command()
@click.argument('name')
def dockerfile(name):
    "Inspect your image from your local dockerfile. The name must be between 2 and 255 letters."
    os.system(("docker build . -t "+name))
    os.system(("docker inspect "+name+' > inspect.json'))
    syft = os.popen(('syft '+name+' -o cyclonedx-json')).read()
    syft_parser.parse_data(syft, 'result.json')
    morph_kgc.materialize('config.ini')


@cli.command()
@click.argument('name1')
@click.argument('name2')
def compare(name1, name2):
    """ Inspect your image from its name or ID """
    os.system(('docker inspect '+ name1+' > inspect1.json'))
    os.system(('docker inspect '+ name2+' > inspect2.json'))
    syft1 = os.popen(('syft '+name1+' -o cyclonedx-json')).read()
    syft2 = os.popen(('syft '+name2+' -o cyclonedx-json')).read()
    syft_parser.parse_data(syft1, 'result1.json')
    syft_parser.parse_data(syft2, 'result2.json')
    morph_kgc.materialize('config1.ini')
    morph_kgc.materialize('config2.ini')


if __name__ == '__main__':
    cli()
