import enum
import click
import os 
import syft_parser as syft_parser 
import morph_kgc
import shutil 
import tempfile


def get_graph(name, save, i, output_path):#, temp_folder:tempfile.TemporaryDirectory):

    """
    to do
    """
    temp_folder = os.makedirs("tmp", exist_ok=True)
    os.system(('docker inspect '+ name+' > '+ os.path.join("tmp" ,'inspect1.json')))
    if save:
        open(os.path.join(output_path ,'inspect'+str(i)+'.json'), 'x')
        shutil.copy(os.path.join("tmp" ,'inspect1.json'), os.path.join(output_path ,'inspect'+str(i)+'.json'))
    syft = os.popen(('syft '+name+' -o cyclonedx-json')).read()
    syft_parser.parse_data(syft, os.path.join("tmp" ,'result1.json'), os.path.join("tmp" ,'inspect1.json'))
    if save:
        open(os.path.join(output_path ,'result'+str(i)+'.json'), 'x')
        shutil.copy(os.path.join("tmp" ,'result1.json'), os.path.join(output_path ,'result'+str(i)+'.json'))
        # Read in the file
    # with open(os.path.join("tmp" ,'config.ini'), 'r') as file :
    #     filedata = file.read()
    # # Replace the target string
    # filedata = filedata.replace('DIRECCION', "tmp" +'mapping.ttl' )
    # # Write the file out again
    # with open(os.path.join("tmp" ,'config.ini'), 'w') as file:
    #     file.write(filedata)
    current_directory = os.getcwd()
    g = morph_kgc.materialize('./tmp/config.ini')
    print('acaba')
    g.serialize(destination=os.path.join("tmp" ,"grafo"+str(i)+".nt"), format="ntriples")
    with open(os.path.join(output_path,"final_result.nt"), "a") as new_file:
        with open(os.path.join("tmp","grafo"+str(i)+".nt"), 'r') as f:
            for line in f:
                new_file.write(line)
            new_file.write("\n")




def temp_dir(name, save, i, output_file):
    temp = os.mkdir("tmp")#tempfile.TemporaryDirectory(dir = os.path.dirname(os.getcwd()))
    f = open(os.path.join("tmp" ,'mapping.ttl'), 'x')
    shutil.copy('../mappings/mapping2.ttl', os.path.join("tmp" ,'mapping.ttl'))
    f.close()
    f1 = open(os.path.join("tmp" ,'config.ini'), 'x')
    shutil.copy(os.path.join('../config.ini'), os.path.join("tmp" ,'config.ini'))
    f1.close()
    get_graph(name, save, i, output_file)#, temp)
    shutil.rmtree('tmp')
    print('DONE')


@click.group()
def cli():
    '''This is a tool for your docker containers.'''
    pass


@cli.command()
@click.option('-p', '--input_path', type=str, help="input path of the file or directory with the name or ID of the images to inspect.")
@click.option('-i', '--input_image', type=str, help="name or ID of the image to inspect")
@click.option('-s', '--save', type=bool, is_flag=True, help="saves temporal json archives in a new directory")
@click.option('-o', '--output_path', type=str ,help="output directory path to store results. If the directory does not exist, the tool will create it.")
def image(input_path, input_image, save, output_path):
    """ Inspect y:our image or images from its name or ID;"""
    os.mkdir(output_path)
    open(output_path+'/final_result.nt', 'x')
    if input_path:
        if os.path.isfile(input_path):
            with open(input_path,'r') as fp:
                names = [elem.rstrip() for elem in fp.readlines()]
                for i,elem in enumerate(names):
                    
                    if save:
                        temp_dir(elem, True, i, output_path)
                    else:
                        temp_dir(elem, False, i, output_path)
        else:
            print('The file does not exists')
    if input_image:
        if save:
            temp_dir(input_image, True, 0, output_path)
        else:
            temp_dir(input_image, False, 0, output_path)



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
    morph_kgc.materialize('./tmp/config.ini')


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
