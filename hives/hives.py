"""
A script for quickly interacting with UC Berkeley's hive machines.
(Every hive in Hives.HIVE_IDS must be authenticated beforehand for this script to work!)


Commands:
    status
        Displays your course, code, and password.

    set <NAME> <VALUE>
        NAME can be 'course', 'code', or 'password'. Stores VALUE in variable NAME.

    ssh
        SSH's into a hive machine using your stored information. Rotates through a list
        of hive machines to avoid getting stuck.

    push <DIR>/<FOLDER>
        Recursively SCP's './DIR/FOLDER' into '~/DIR/FOLDER' on the hive machine. Errors if
        DIR does not already exist on the hive machine.
"""

import os
import sys
import pickle
import time
import keyboard
from threading import Thread


class Hives:
    HIVE_IDS = [
        'hive4',  'hive5',  'hive6',  'hive7',  'hive8',
        'hive9',  'hive10', 'hive11', 'hive12', 'hive13',
        'hive14', 'hive15', 'hive16', 'hive17', 'hive18',
        'hive19', 'hive20'
    ]

    def __init__(self):
        self.index = 0
        self.course = ''
        self.code = ''
        self.password = ''

    def __next__(self):
        if self.index >= len(Hives.HIVE_IDS):   # HIVE_IDS may be edited between calls to hives.py
            self.index = 0
        result = Hives.HIVE_IDS[self.index]
        self.index = (self.index + 1) % len(Hives.HIVE_IDS)
        return result

    def __str__(self):
        return f"course='{self.course}'\n" \
               f"code='{self.code}'\n" \
               f"password='{self.password}'"

    def save(self):
        target = open('.hives', 'wb')
        pickle.dump(self, target)

    @staticmethod
    def load():
        if not os.path.exists('.hives'):
            Hives().save()
        target = open('.hives', 'rb')
        return pickle.load(target)


def check(condition, message=''):
    if not condition:
        print(message)
        exit(0)


if __name__ == '__main__':
    check(len(sys.argv) > 1, "Please input a command.")
    command = sys.argv[1].lower()
    args = sys.argv[2:]

    hives = Hives.load()

    if command == 'status':
        print(hives)
        exit(0)
    elif command == 'set':
        check(len(args) == 2, 'Must have two arguments: NAME, VALUE')
        if args[0] == 'course':
            hives.course = args[1]
        elif args[0] == 'code':
            hives.code = args[1]
        elif args[0] == 'password':
            hives.password = args[1]
        else:
            print(f"'{args[0]}' is not a valid setting.")
            exit(0)
        print(f"Updated '{args[0]}' to '{args[1]}'.")
        hives.save()
        exit(0)

    check(hives.course, "Course has not been set.")
    check(hives.code, "Code has not been set.")

    cli_command = ''
    if command == 'ssh':
        cli_command = f'ssh {hives.course}-{hives.code}@{next(hives)}.cs.berkeley.edu'
    elif command == 'push':
        check(len(args) == 1, 'Must have exactly one argument: PATH.')
        path = args[0]
        exclude = {'/', '\\'}

        end = len(path) - 1
        while path[end] in exclude:
            end -= 1

        start = end
        while path[start] not in exclude:
            start -= 1

        folder = path[start+1:end+1]
        rest = path[:start+1]

        cli_command = f'scp -r {rest}/{folder} ' \
                      f'{hives.course}-{hives.code}@{next(hives)}.cs.berkeley.edu:~/{rest}/'
    else:
        print(f"'{command}' is an unrecognized command.")
        exit(0)

    hives.save()

    check(hives.password, "Password has not been set.")

    def execute():
        os.system(cli_command)
        exit(0)

    thread = Thread(target=execute)
    thread.daemon = True
    thread.start()

    keyboard.write(hives.password)
    keyboard.press('Enter')

    while thread.is_alive():
        time.sleep(0.1)
