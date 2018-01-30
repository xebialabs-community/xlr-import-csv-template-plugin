#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json, sys

from csv_import.CsvParser import CsvParser
from csv_import.XlReleaseClient import XlReleaseClient


for item in request.entity:
    if item['name'] == 'csv':
        csv_str = str(item['value'])
    if item['name'] == 'template_name':
        template_name = item['value']

try: 
    tasks = CsvParser(csv_str).parse()
    xlr_client = XlReleaseClient(templateApi, phaseApi, taskApi)
    template = xlr_client.create_blank_template(template_name)
    xlr_client.add_tasks_to_template(template, tasks)
    xlr_client.add_teams_to_template(template, tasks)

    response.statusCode = 201
    response.entity = {
        "id": template.id,
        "message": "Successfully imported template [%s]" % template_name
    }

except (RuntimeError, TypeError, NameError) as e:
    logger.error("Unexpected error:", str(e))
    print str(e)

    response.statusCode = 500
    response.entity = {"result": "Error importing template [%s]" % str(e)}
except:
    message = "Unexpected error: [%s]" % str(sys.exc_info())
    logger.error(message)
    print message

    response.statusCode = 500
    response.entity = {"result": "Error importing template [%s]" % message}

