import json
import os

def json_to_dict(json_as_string):
    '''
    Loads json from string and return it in dict type
    json_as_string := str
    '''
    
    a = json.loads(json_as_string) 
    return a


def dict_to_json(path, data):
    '''
    Save data (dict) to json file,
    path must include .json

    data := dict
    path := str
    '''
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    return 200


def read_inspect_id(path):
    '''
    Gets image_id form  inspect.json

    inspect_path := str
    '''
    #open file

    with open(path,'r') as fp:

        a = json.load(fp)[0]

    #get image_id
    image_id = a['Id']

    return image_id

def parse_data(json_as_string, path_output, path):
    '''
    Parse data from path_input to path_output
    json_as_string := str
    path_output := str
    '''
    data = json_to_dict(json_as_string)

    data_parsed = data.copy()
    i = 'components'
    k = 'properties'

    for j,_ in enumerate(data[i]): #enumerate components
        layer_list = []
        
        for l_1, _ in enumerate(data[i][j]['properties']): # enumerate properties
            aux_key = data[i][j]['properties'][l_1]['name']
            aux_value = data[i][j]['properties'][l_1]['value']
            if 'layerID' in aux_key:
                layer_list.append(aux_value)
            else:
                data_parsed[i][j][aux_key] = aux_value

        if 'externalReferences' in data[i][j].keys():
            for l_2, _ in enumerate(data[i][j]['externalReferences']): # enumerate properties
                aux_key = data[i][j]['externalReferences'][l_2]['type']
                aux_value = data[i][j]['externalReferences'][l_2]['url']
                data_parsed[i][j][aux_key] = aux_value
            data_parsed[i][j].pop('externalReferences')

        data_parsed[i][j]['image_identifier'] = read_inspect_id(path) 
        data_parsed[i][j].pop('properties')
        

        if len(layer_list)>0:
            data_parsed[i][j]['layersId'] = layer_list

    

    dict_to_json(path=path_output, data=data_parsed)


    return 200

######### delete when tested ###############
def  main():
    path_input='result1.json'
    path_output='widoco_test_8.json' 
    parse_data(path_input= "widoco.json", path_output="cleanwidoco.json")

if __name__ == '__main__':
    main()
    