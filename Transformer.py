import os
import sys
import base64
import time
import datetime
from datetime import timedelta
from github import Github
from Print import Print
from Env import env

print = Print() # add glorious indentation and colors to print

class Transformer(object):
    def __init__(self):
        pass

    def regex_for(self, type):
        expressions = {
            "table": r'Schema::create\(',
            "data_type": r'\$table->',
        }

        return expressions[type]

    # testing a cleaner interface
    def __getattr__(self, name):
        if name.startswith('regex_for_'):
            return self.regex_for(
                    name.split("regex_for_",1)[1] 
            )
        raise Exception('No such method')

if __name__ == '__main__':
    # Demo of the class 
    t = Transformer()
    print(t.regex_for_table)
