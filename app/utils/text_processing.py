import json

def processJson(data_string):
    print("before-")
    print(data_string)
    print(type(data_string))

    data_string = data_string[7:]
    
    data_string = data_string[:-3]
    
    transformed_string = '{ "medData": ' + data_string + ' }'
    
    return json.loads(transformed_string)