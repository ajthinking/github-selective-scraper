import os
import sys
import base64
import time
import datetime
import re
import inspect
from datetime import timedelta
from github import Github

# Add parent src hack 
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))

from Print import Print #pylint: disable=E0401


print = Print() # add glorious indentation and colors to print


class MigrationFile(object):
    def __init__(self, path):
        self.path = path
        with open(path) as file:
            self.content = file.read()
            self.table = self.find_table()
            self.column_definitions = self.find_column_definitions()
            self.extract_path_data(path)

    def extract_path_data(self, path):
            parts = path.split('/')
            self.name = parts[-1]
            self.repo = parts[-4]
            self.user = parts[-5]

    def find_table(self):
        matches = re.findall(
                self.regex_for_table,
                self.content
        )

        # Dont accept multiple table creations in the same file
        if len(matches) != 1:
            return False

        return matches[0]        

    def qualifies(self):
        return bool(self.table) and True

    def find_column_definitions(self):
        data_types = re.findall(
                self.regex_for_column_data_type,
                self.content
        )

        names = re.findall(
                self.regex_for_column_name,
                self.content
        )

        if len(data_types) != len(names):
            return []        

        return zip(data_types, names)


    def regex_for(self, type):
        expressions = {
            "table": r"(?:Schema::create\(')(.*)(?:')",
            "column_data_type": r"(?:\$table->)([a-zA-Z1-9_]*)",
            "column_name": r"(?:\$table->)(?:[a-z_A-Z]*)\('([a-zA-Z1-9_]*)",
        }
        return expressions[type]

    def __getattr__(self, name):
        if name.startswith('regex_for_'):
            return self.regex_for(
                    name.split("regex_for_",1)[1] 
            )
        raise Exception('No such method') 

    # todo
    def tokenize(self):
        pass

if __name__ == '__main__':
    # Demo of the class 
    pass
