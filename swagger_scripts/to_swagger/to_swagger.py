import os
import json
from urllib.parse import urlparse, parse_qs

MAX_LIST_LEN = 3
MAX_STR_LEN = 32
TYPES = {
    type(None): 'object',
    str: 'string',
    int: 'integer',
    bool: 'boolean',
    float: 'float',
    dict: 'object',
    list: 'array'
}


def clean(obj):
    t = type(obj)
    if t is str and len(obj) > MAX_STR_LEN:
        obj = obj[:MAX_STR_LEN] + '...'
    elif t is list:
        obj = [clean(x) for x in obj[:MAX_LIST_LEN]]
    elif t is dict:
        obj = {k: clean(v) for k, v in obj.items()}
    return obj


def convert(obj, set_example):
    t = type(obj)
    converted = {
        'type': TYPES[t]
    }

    # Recurse if needed
    if t is dict:
        converted['required'] = list(obj.keys())
        converted['properties'] = {k: convert(v, set_example) for k, v in obj.items()}
    elif t is list:
        if len(obj) > 0:
            converted['items'] = convert(obj[0], False)

    # Set example if needed
    if t is not dict and set_example:
        converted['example'] = obj
    return converted


if __name__ == '__main__':
    #############
    #   Name    #
    #############
    if not os.path.exists('name.txt'):
        with open('name.txt', 'w'):
            pass
    with open('name.txt', 'r') as file:
        name = file.read()

    #############
    #    URL    #
    #############
    if not os.path.exists('url.txt'):
        with open('url.txt', 'w'):
            pass
    with open('url.txt', 'r') as file:
        url = file.read()

    #################
    #   Request     #
    #################
    if not os.path.exists('request.json'):
        with open('request.json', 'w'):
            pass
    with open('request.json', 'r') as file:
        request = json.load(file)
        assert type(request) is dict, 'Request JSON must be a dictionary'

    #################
    #   Response    #
    #################
    if not os.path.exists('response.json'):
        with open('response.json', 'w'):
            pass
    with open('response.json', 'r') as file:
        response = json.load(file)
        assert type(response) is dict, 'Response JSON must be a dictionary'

    cleaned = clean(response)
    schema = convert(cleaned, True)
    result = {
        'tags': [],
        'summary': '',
        'description': '',
        'consumes': [''],
        'responses': {
            '0': {
                'description': 'Successful operation',
                'schema': schema
            }
        }
    }
    string = (
        json.dumps(result, indent=4)
        .replace('true', 'True')
        .replace('false', 'False')
        .replace('null', 'None')
    )

    with open('out.py', 'w') as file:
        file.write(f'{name}_swagger = ' + string + '\n')
