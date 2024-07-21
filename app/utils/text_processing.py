import json
import re

def processJson(data_string):
    print("before-")
    print(data_string)
    print(type(data_string))

    pattern = r'```json(.*?)```'
    match = re.search(pattern, data_string, re.DOTALL)

    extracted_string = ""
    if match:
        extracted_string = match.group(1).strip()
    else:
        print("No match found.")
        return False, ""
    
    transformed_string = '{ "medData": ' + extracted_string + ' }'

    try:
        parsed_data = json.loads(transformed_string)
        return True, parsed_data
    except json.JSONDecodeError as e:
        print("Parsing failed:")
        print(f"Error: {e}")
        return False, ""
