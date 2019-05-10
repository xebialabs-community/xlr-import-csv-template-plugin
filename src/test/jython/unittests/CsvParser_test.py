#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import unittest

from csv_import.CsvParser import CsvParser

class ImportCsv(unittest.TestCase):

	# technically, this is a shitty unittest, it's more an integration test
	def test_parse(self):
		tasks = []
		with open('src/test/jython/unittests/sample_release.csv', 'rb') as csv_str:
			tasks = CsvParser(csv_str.read()).parse()

		self.assertEqual(len(tasks), 33)


	def test_should_not_fail_on_empty(self):
		csv_str = """


"""
		
		tasks = CsvParser(csv_str).parse()
		self.assertEqual(len(tasks), 0)


	def test_should_ignore_rows_with_too_little_columns(self):
		csv_str = """
QA		PLANNED		09-12-17 14:50	09-12-17 07:00	09-12-17 14:50	7h 50m
Wait for dependencies	Gate	PLANNED			09-12-17 07:00	09-12-17 08:00	1h
"""
		tasks = CsvParser(csv_str).parse()
		self.assertEqual(len(tasks), 0)


	def test_should_fail_on_tasks_without_phase_before_it(self):
		csv_str = """
Wait for dependencies	Gate	PLANNED			09-12-17 07:00	09-12-17 08:00	1h				No	0
"""
		with self.assertRaises(Exception) as cm:
			tasks = CsvParser(csv_str).parse()

		self.assertEqual(cm.exception.message, "Expect a phase name by now - something wrong with the sheet")


	def test_should_parse_task_with_correct_phase(self):
		csv_str = """
QA		PLANNED		09-12-17 14:50	09-12-17 07:00	09-12-17 14:50	7h 50m					
Wait for dependencies	Gate	PLANNED			09-12-17 07:00	09-12-17 08:00	1h		team1		No	0
UAT		PLANNED			09-12-17 14:50	09-12-17 22:51	8h 1m					
Acceptance environment available	Manual	PLANNED			09-12-17 14:50	09-12-17 15:50	1h		team2		No	0
"""
		tasks = CsvParser(csv_str).parse()

		self.assertEqual(len(tasks), 2)
		
		task = tasks[0]
		self.assertEqual(task['phase_name'], "QA")
		self.assertEqual(task['title'], "Wait for dependencies")
		self.assertEqual(task['type'], "Gate")
		self.assertEqual(task['team'], "team1")
		self.assertEqual(task['description'], "")

		task2 = tasks[1]
		self.assertEqual(task2['phase_name'], "UAT")
		self.assertEqual(task2['title'], "Acceptance environment available")
		self.assertEqual(task2['type'], "Manual")
		self.assertEqual(task2['team'], "team2")
		self.assertEqual(task2['description'], "")


