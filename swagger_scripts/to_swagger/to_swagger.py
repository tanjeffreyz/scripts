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


def transfer(obj, prev):
    if type(obj) is list and type(prev) is list:
        # Map properties of prev by name
        prev_map = {x['name']: x for x in prev if 'name' in x}

        # Only recurse on properties in obj that are also preset in prev
        for i in range(len(obj)):
            if type(obj[i]) is dict and 'name' in obj[i]:
                name = obj[i]['name']
                if name in prev_map:
                    transfer(obj[i], prev_map[name])
    elif type(obj) is dict and type(prev) is dict:
        if 'description' in prev:
            desc = prev['description']
            if type(desc) is str:
                obj['description'] = desc
        for key in obj:
            if key in prev:
                transfer(obj[key], prev[key])


if __name__ == '__main__':
    if not os.path.exists('prev.py'):
        with open('prev.py', 'w') as file:
            file.write('default = {}\n')

    import prev
    variables = [x for x in dir(prev) if not x.startswith('_')]
    assert len(variables) == 1, 'prev.py must only contain 1 variable'
    name = variables[0]
    prev_swagger = prev.__dict__[name]
    assert type(prev_swagger) is dict, 'prev.py must contain a dictionary'

    #############
    #    URL    #
    #############
    if not os.path.exists('url.txt'):
        with open('url.txt', 'w') as file:
            file.write('https://www.google.com?param=default')
    with open('url.txt', 'r') as file:
        url = file.read()

    parameters = [
        {
            'name': 'Authorization',
            'in': 'header',
            'description': 'Authorization (Only:Your-Ridgebot-User-Token)',
            'required': True,
            'type': 'string',
            'default': 'Your-Ridgebot-User-Token'
        }
    ]
    for k, v in parse_qs(urlparse(url).query).items():
        # Convert v to appropriate type
        v = v[0].strip()
        if v.lower() == 'true':
            v = True
        elif v.lower() == 'false':
            v = False
        else:
            try:
                v = int(v)
            except ValueError:
                try:
                    v = float(v)
                except ValueError:
                    pass

        t = type(v)
        parameters.append({
            'name': k,
            'in': 'query',
            'required': True,
            'type': TYPES[t],
            'default': t(),
            'example': v
        })

    #################
    #   Payload     #
    #################
    if not os.path.exists('payload.json'):
        with open('payload.json', 'w') as file:
            pass
    with open('payload.json', 'r') as file:
        contents = file.read()
        payload = json.loads(contents) if len(contents) > 0 else {}
        assert type(payload) is dict, 'Payload JSON must be a dictionary'

    consumes = 'text/plain'
    if len(payload) > 0:
        cleaned = clean(payload)
        schema = convert(cleaned, True)
        parameters.append({
            'name': 'root',
            'in': 'body',
            'schema': schema
        })
        consumes = 'application/json'

    #################
    #   Response    #
    #################
    if not os.path.exists('response.json'):
        with open('response.json', 'w') as file:
            pass
    with open('response.json', 'r') as file:
        contents = file.read()
        response = json.loads(contents) if len(contents) > 0 else {}
        assert type(response) is dict, 'Response JSON must be a dictionary'

    cleaned = clean(response)
    schema = convert(cleaned, True)
    result = {
        'tags': prev_swagger.get('tags', ['']),
        'summary': prev_swagger.get('summary', ''),
        'description': prev_swagger.get('description', ''),
        'consumes': [consumes],
        'parameters': parameters,
        'responses': {
            '200': {
                'description': 'Successful operation',
                'schema': schema
            }
        }
    }
    transfer(result, prev_swagger)
    string = (
        json.dumps(result, indent=4)
        .replace('true', 'True')
        .replace('false', 'False')
        .replace('null', 'None')
    )

    with open('out.py', 'w') as file:
        file.write(f'{name.strip()} = ' + string.strip() + '\n')
