import json

def json_to_dict(path):
    '''
    Loads json from path and return it in dict type
    path := str
    '''
    
    a = json.loads(path) 
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
def parse_data(path_input, path_output):
    '''
    Parse data from path_input to path_output
    path_input := str
    path_output := str
    '''
    data = json_to_dict(path=path_input)

    data_parsed = data.copy()
    i = 'components'
    k = 'properties'

    for j,_ in enumerate(data[i]): #enumerate components
        for l, _ in enumerate(data[i][j][k]): # enumerate properties
            aux_key = data[i][j][k][l]['name']
            aux_value = data[i][j][k][l]['value']
            data_parsed[i][j][aux_key] = aux_value

    dict_to_json(path=path_output, data=data_parsed)

    return 200

######### delete when tested ###############
def  main():
    path_input='widoco_test.json'
    path_output='widoco_test_8.json' 
    parse_data(path_input=path_input, path_output=path_output)

if __name__ == '__main__':
    main()
    