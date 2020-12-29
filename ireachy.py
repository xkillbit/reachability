#! /usr/bin/python3

from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import os
import regex

class FileNameValidator(Validator):
        def validate(self, document):
            files_in_dir= os.listdir('.')
            if document.text not in files_in_dir:
                raise ValidationError(message='[ERROR] Input file does not exist in current directory that ireach.py is running in. Try again.', cursor_position=len(document.text))  # Move cursor to end

questions = [
    {
        'type': 'input',
        'name': 'ranges_to_scan',
        'message': 'What file contians your list of ranges?',
        'validate': FileNameValidator
        
    },
    {
        'type':'list',
        'name':'speed_to_scan',
        'message':'How Fast? (Packets Per Seconds)',
        'choices':['100','1000','10000','100000','200000'],
        'filter':lambda val: val.lower()
    }
]

answers = prompt(questions)
print('\nScanning Ranges in file named, "',answers['ranges_to_scan'],'" at a rate of ', answers['speed_to_scan'],' packets per second.\n')  # use the answers as input for your app

command2run='python3 reachy.py '+answers['ranges_to_scan']+' '+answers['speed_to_scan']
os.system(command2run)

