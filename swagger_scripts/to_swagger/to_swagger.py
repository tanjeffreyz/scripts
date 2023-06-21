import json

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


with open('in.json', 'r') as file:
    obj = json.load(file)
    assert type(obj) is dict, 'JSON object must be a dictionary'

cleaned = clean(obj)
converted = convert(cleaned, True)
pretty = (
    json.dumps(converted, indent=4)
    .replace('true', 'True')
    .replace('false', 'False')
    .replace('null', 'None')
)

with open('out.py', 'w') as file:
    file.write('schema = ' + pretty + '\n')
