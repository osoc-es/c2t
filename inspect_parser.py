import json

def json_to_dict(path):
    '''
    Loads json from path and return it in dict type
    path := str
    '''
    with open(path,'r') as fp:
        a = json.load(fp)[0]  
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

    final_result = dict()
    data_filter = ['Id','Os','Architecture','Layers']

    for i in data.keys():
        if i in data_filter:
            final_result[i] = data[i]
        try:
            for j in data[i].keys():
                if j in data_filter:
                    counter =1
                    for k in data[i][j]:
                        index = f'layer_{counter}'
                        final_result[index] = k
                        counter += 1
        except:
            None

    dict_to_json(path=path_output, data=final_result)

    return 200

######### delete when tested ###############
def  main():
    path_input='data.json'
    path_output='data_parsed.json' 
    parse_data(path_input=path_input, path_output=path_output)

if __name__ == '__main__':
    main()
    