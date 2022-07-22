![logo](onto_documentation/images/logo.png)
What we do is transform docker images into knowledge graphs.
## Installation
For using this repo we asume that you have installed:
- [docker](https://docs.docker.com/engine/install/)
- [syft](https://github.com/anchore/syft)
- [python 3.10.4](https://www.python.org/downloads/release/python-3104/)

## Usage
To create your knowledge graph from your Docker container you must run one of these commands. 

To create the graph from a local image:

To create the graph from a file with a list of local images that may be 

To create the graph from a DockerHub image:

To create the graph from a file with a list of DockerHub images (the file must have this format: 

"mongo:latest

python:3.10 

mysql:latest"):

To create the graph from a DockerFile:



Para crear el grafo a partir de una imagen en local: 

Para crear el grafo a partir de una lista de imágenes en local (tiene que estar en un fichero):

Para ... a partir de una imagen de DockerHub 

Para ... a partir de un DockerFile 
``` bash
CLI.py image {name} {output}
```
DockerHub images
``` bash
CLI.py dockerhub {name} {output}
```
DockerFiles
``` bash
CLI.py dockerfile {name} {output}
```

## How it works
We inspect your image to get enviroment properties. Then we use syft to obtain the image dependencies. After that we have to [transform](syft_parser.py) a bit the output.

Once we have these data sources, we have to create a knowledge graph. For this purpose we will use [morphkgc](https://github.com/oeg-upm/morph-kgc)

## Ontology Documentation
Available here: [https://osoc-es.github.io/c2t/onto_documentation/index-en.html](https://osoc-es.github.io/c2t/onto_documentation/index-en.html)

## Landing Page
Available here: [https://osoc-es.github.io/c2t/website](https://osoc-es.github.io/c2t/website)

## Ontology diagram
![onto_map](onto_documentation/images/diagram.svg)
