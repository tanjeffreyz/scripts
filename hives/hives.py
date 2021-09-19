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

    push <DIR> <FOLDER>
        Recursively SCP's './DIR/FOLDER' into '~/DIR/FOLDER' on the hive machine. Errors if
        DIR does not exist on the hive machine.
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
        'hive19', 'hive20', 'hive21', 'hive22', 'hive23',
        'hive24', 'hive25', 'hive26', 'hive27', 'hive28',
        'hive29', 'hive30'
    ]

    def __init__(self):
        self.index = 0
        self.course = ''
        self.code = ''
        self.password = ''

    def __next__(self):
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
    flag = sys.argv[1].lower()
    args = sys.argv[2:]

    commands = ''
    hives = Hives.load()

    if flag == 'status':
        print(hives)
        exit(0)
    elif flag == 'set':
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

    if flag == 'ssh':
        commands = f'ssh {hives.course}-{hives.code}@{next(hives)}.cs.berkeley.edu'
    elif flag == 'push':
        check(len(args) == 2, 'Must have exactly two arguments: DIR, FOLDER.')
        commands = f'scp -r {args[0]}/{args[1]} ' \
                   f'{hives.course}-{hives.code}@{next(hives)}.cs.berkeley.edu:~/{args[0]}/'
    else:
        print(f"'{flag}' is an unrecognized command.")
        exit(0)

    hives.save()

    check(hives.password, "Password has not been set.")

    def execute():
        os.system(commands)
        exit(0)

    thread = Thread(target=execute)
    thread.daemon = True
    thread.start()

    keyboard.write(hives.password)
    keyboard.press('Enter')

    while thread.is_alive():
        time.sleep(0.1)
