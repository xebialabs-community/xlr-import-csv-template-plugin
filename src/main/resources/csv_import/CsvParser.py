#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import csv

class CsvParser:
    def __init__(self, csv_str):
        self.csv_str = csv_str
        self.field_to_column_index_mapping = {
            'phase_name': 0,
            'title': 1,
            'description': 5,
            'team': 6
        }
    
    def parse(self):
        parsed_tasks = []
        template_reader = csv.reader(self.csv_str.split('\n'), delimiter='\t', dialect='excel', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in template_reader:
            if len(row) < max(self.field_to_column_index_mapping.values()):
                logger.warn('Skipping row [%s] due to too little columns' % row)
                continue

            task = {}
            task['phase_name'] = row[self.field_to_column_index_mapping['phase_name']]
            task['title'] = row[self.field_to_column_index_mapping['title']]
            task['description'] = row[self.field_to_column_index_mapping['description']]
            task['team'] = row[self.field_to_column_index_mapping['team']]
            
            parsed_tasks.append(task)

        return parsed_tasks