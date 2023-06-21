import json

IGNORED = {'logo', 'desc'}
MAX_LIST_LEN = 3
MAX_STR_LEN = 32


def clean(obj):
    if type(obj) is str:
        if len(obj) > MAX_STR_LEN:
            obj = obj[:MAX_STR_LEN] + '...'
        return obj
    elif type(obj) is list:
        arr = [clean(x) for x in obj[:MAX_LIST_LEN]]
        num_hidden = len(obj) - MAX_LIST_LEN
        if num_hidden > 0:
            arr.append(f'({num_hidden} more item{"s" if num_hidden > 1 else ""} not shown)')
        return arr
    elif type(obj) is dict:
        return {k: ('...' if k in IGNORED else clean(v)) for k, v in obj.items()}
    return obj


if __name__ == '__main__':
    with open('target.json', 'r') as file:
        contents = json.loads(file.read())

    contents = clean(contents)

    with open('target.json', 'w') as file:
        file.write(json.dumps(contents, sort_keys=True, indent=2) + '\n')
