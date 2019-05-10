#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import csv
import csv_import

class CsvParser:
    def __init__(self, csv_str):
        self.csv_str = csv_str
        self.field_to_column_index_mapping = {
            'title_or_phase': 0,
            'type': 1,
            'team': 9
        }
        self.delimiter = '\t'
        self.dialect = 'excel'
        self.quotechar = '"'
        self.quoting = csv.QUOTE_MINIMAL
        self.line_separator = '\n'
        self.logger = csv_import.getLogger()

    def is_phase_row(self, row):
        task_type = row[self.field_to_column_index_mapping['type']]
        if task_type:
            return False
        return True
    
    def parse(self):
        parsed_tasks = []
        template_reader = csv.reader(
            self.csv_str.split(self.line_separator), 
            delimiter=self.delimiter, 
            dialect=self.dialect, 
            quotechar=self.quotechar, 
            quoting=self.quoting
        )

        phase_name = None
        for row in template_reader:
            if len(row) < max(self.field_to_column_index_mapping.values()):
                self.logger.debug('Too little columns, skipping: row [%s]' % row)
                continue

            title_or_phase = row[self.field_to_column_index_mapping['title_or_phase']]
            if not title_or_phase:
                self.logger.debug('Empty title_or_phase, skipping: row [%s]' % row)
                continue

            if self.is_phase_row(row):
                phase_name = title_or_phase
                continue

            if not phase_name:
                message = "Expect a phase name by now - something wrong with the sheet"
                self.logger.error(message)
                raise Exception("Expect a phase name by now - something wrong with the sheet")

            task = {}
            task['phase_name'] = phase_name
            task['description'] = ''
            task['title'] = title_or_phase
            task['type'] = row[self.field_to_column_index_mapping['type']]
            task['team'] = row[self.field_to_column_index_mapping['team']]
            
            parsed_tasks.append(task)

        return parsed_tasks

