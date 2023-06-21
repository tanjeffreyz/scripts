import json


def compare(before_obj, after_obj, string, new, removed):
    if type(before_obj) is not dict or type(after_obj) is not dict:
        return
    if string != '':
        string += '.'
    for key in before_obj.keys() | after_obj.keys():
        new_string = string + key
        if key not in before_obj:
            new.append(new_string)
        elif key not in after_obj:
            removed.append(new_string)
        else:
            compare(before_obj[key], after_obj[key], new_string, new, removed)


if __name__ == '__main__':
    with open('before.json', 'r') as file:
        before_obj = json.loads(file.read())

    with open('after.json', 'r') as file:
        after_obj = json.loads(file.read())

    new = []
    removed = []
    compare(before_obj, after_obj, '', new, removed)

    print('\nRequest:')
    print(f"New: {', '.join(new)}")
    print(f"Removed: {', '.join(removed)}")
    print()
    print('Response:')
