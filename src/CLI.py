import click
import os

from numpy import require 
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
        open(os.path.join(output_path ,'result_inspect_'+str(i)+'.json'), 'w')
        shutil.copy(os.path.join("tmp" ,'inspect1.json'), os.path.join(output_path ,'result_inspect_'+str(i)+'.json'))
    syft = os.popen(('syft '+name+' -o cyclonedx-json')).read()
    syft_parser.parse_data(syft, os.path.join("tmp" ,'result1.json'), os.path.join("tmp" ,'inspect1.json'))
    if save:
        open(os.path.join(output_path ,'result_syft_'+str(i)+'.json'), 'w')
        shutil.copy(os.path.join("tmp" ,'result1.json'), os.path.join(output_path ,'result_syft_'+str(i)+'.json'))
    g = morph_kgc.materialize('./tmp/config.ini')
    g.serialize(destination=os.path.join("tmp" ,"grafo"+str(i)+".nt"), format="ntriples")
    with open(os.path.join(output_path,"final_result.nt"), "a") as new_file:
        with open(os.path.join("tmp","grafo"+str(i)+".nt"), 'r') as f:
            for line in f:
                new_file.write(line)
            new_file.write("\n")




def temp_dir(name, save, i, output_file):
    temp = os.makedirs("tmp",exist_ok=True)#tempfile.TemporaryDirectory(dir = os.path.dirname(os.getcwd()))
    try:
        f = open(os.path.join("tmp" ,'mapping.ttl'), 'w')
        shutil.copy('../mappings/mapping_complete.ttl', os.path.join("tmp" ,'mapping.ttl'))
        f.close()
        f1 = open(os.path.join("tmp" ,'config.ini'), 'w')
        shutil.copy(os.path.join('../config.ini'), os.path.join("tmp" ,'config.ini'))
        f1.close()
        get_graph(name, save, i, output_file)#, temp)
        shutil.rmtree('tmp')
    except:
        shutil.rmtree('tmp')


@click.group()
def cli():
    '''This is a tool for your docker containers.'''
    pass


@cli.command()
@click.option('-p', '--input_path', type=str, help="input path of the file or directory with the name or ID of the images to inspect.")
@click.option('-i', '--input_image', type=str, help="name or ID of the image to inspect")
@click.option('-s', '--save', type=bool, is_flag=True, help="saves temporal json archives in a new directory")
@click.option('-o', '--output_path', type=str , required= True, help="output directory path to store results. If the directory does not exist, the tool will create it.")
def image(input_path, input_image, save, output_path):
    """ Inspect y:our image or images from its name or ID;"""    
    os.makedirs(output_path, exist_ok=True)
    f = open(output_path+'/final_result.nt', 'w')
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
    f.close()



@cli.command()
@click.option('-p', '--input_path', type=str, help="input path of the file or directory with the name of the images to inspect in dockerhub.")
@click.option('-i', '--input_image', type=str, help="name or ID of the image to inspect in dockerhub")
@click.option('-s', '--save', type=bool, is_flag=True, help="saves temporal json archives in the output directory")
@click.option('-o', '--output_path', type=str, required= True, help="output directory path to store results. If the directory does not exist, the tool will create it.")
def dockerhub(input_path, input_image, save, output_path):
    """ Inspect an image or images from dockerhub """
    os.makedirs(output_path, exist_ok=True)
    f = open(output_path+'/final_result.nt', 'w')
    if input_path:
        if os.path.isfile(input_path):
            with open(input_path,'r') as fp:
                names = [elem.rstrip() for elem in fp.readlines()]
                for name in names:
                    os.system(('docker pull '+ name))
                for i,elem in enumerate(names):
                    
                    if save:
                        temp_dir(elem, True, i, output_path)
                    else:
                        temp_dir(elem, False, i, output_path)
        else:
            print('The file does not exists')
    if input_image:
        os.system(('docker pull '+ input_image))
        if save:
            temp_dir(input_image, True, 0, output_path)
        else:
            temp_dir(input_image, False, 0, output_path)
    f.close()


@cli.command()
@click.option('-p', '--input_path', type=str, required= True, help="input path of the dockerfile")
@click.option('-i', '--image_name', type=str, required= True, help="name of the image in the dockerfile")
@click.option('-s', '--save', type=bool, is_flag=True, help="saves temporal json archives in the output directory")
@click.option('-o', '--output_path', type=str, required= True, help="output directory path to store results. If the directory does not exist, the tool will create it.")
def dockerfile(input_path, image_name, save, output_path):
    "Inspect your image from your local dockerfile. The name must be between 2 and 255 letters."
    os.makedirs(output_path, exist_ok=True)
    f = open(output_path+'/final_result.nt', 'w')
    print("docker build "+str(input_path)+ " -t "+image_name)
    os.system(("docker build "+str(input_path)+ " -t "+image_name))
    if save:
        temp_dir(image_name, True, 0, output_path)
    else:
        temp_dir(image_name, False, 0, output_path)
    f.close()


if __name__ == '__main__':
    cli()
