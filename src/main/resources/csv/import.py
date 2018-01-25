#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import base64, csv, getpass, json, os.path, sys, urllib2
from sets import Set

#print "CSV File:",
#csv_file = 'sample.csv'
#if not os.path.isfile(csv_file):
#    print "Specified CSV file %s does not exist." % csv_file
#    sys.exit(1)
#print "New Template Name:",
#template_name = raw_input()

from StringIO import StringIO

for item in request.entity:
    if item['name'] == 'csv':
        csv_str = str(item['value'])
    if item['name'] == 'template_name':
        template_name = item['value']
    if item['Authorization']:
        auth_string = item['value']

jythonRequest = request
jythonResponse = response

# Defaults
xlr_url = "http://localhost:5516"
xlr_user = "admin"
xlr_pass = "admin"

opener = urllib2.build_opener(urllib2.HTTPHandler)

data = '''{
  "id" : "Applications/Release1",
  "type" : "xlrelease.Release",
  "title" : "%s",
  "scheduledStartDate" : "2017-10-21T21:05:07.014+02:00",
  "status" : "TEMPLATE"
}''' % template_name

headers = {"Content-Type" : "application/json" , "Authorization" : auth_string}

request = urllib2.Request('%s/api/v1/templates' % xlr_url, data, headers)
response = opener.open(request)

template = json.load(response)

if response.getcode() != 200:
    raise Exception("Failed to create new template: %s" % template_name)

# Delete unnecessary "New Phase"
request = urllib2.Request('%s/api/v1/phases/%s' % (xlr_url, template['phases'][0]['id']), data, headers)
request.get_method = lambda: 'DELETE'
response = opener.open(request)

phases = []
template_reader = csv.reader(csv_str.split('\n'), delimiter='\t', dialect='excel', quotechar='"', quoting=csv.QUOTE_MINIMAL)
for row in template_reader:
    if not row[0] in phases:
        phases.append(row[0])

print phases

phase_name_id_map = {}
for phase_name in phases:
    data = {'id' : '', 'type' : 'xlrelease.Phase', 'title' : phase_name, 'release' : template['id'], 'status' : 'PLANNED'}
    request = urllib2.Request('%s/api/v1/phases/%s/phase' % (xlr_url, template['id']), json.dumps(data), headers)
    response = opener.open(request)
    phase = json.load(response)
    phase_name_id_map[phase_name] = phase['id']
    if response.getcode() != 200:
        raise Exception("Failed to create new phase: %s in template: %s" % (phase_name, template_name))

# Hardcoded, can be parsed from CSV.
teamNames = Set([])

# Create Tasks
template_reader = csv.reader(csv_str.split('\n'), delimiter='\t', dialect='excel', quotechar='"', quoting=csv.QUOTE_MINIMAL)
for row in template_reader:
    phase_id = phase_name_id_map[row[0]]
    data = {'id' : '', 'type' : 'xlrelease.Task', 'title' : row[1], 'description' : row[5]}
    if row[6]:
        data['team'] = row[6]
        teamNames.add(row[6])
    print phase_id
    request = urllib2.Request('%s/api/v1/tasks/%s/tasks' % (xlr_url, phase_id), json.dumps(data), headers)
    response = opener.open(request)
    task = json.load(response)
    if response.getcode() != 200:
        raise Exception("Failed to create new task %s." % row[1])

teams = [
    { "teamName" : template['teams'][0]['teamName'], "id" : template['teams'][0]['id'] },
    { "teamName" : template['teams'][1]['teamName'], "id" : template['teams'][1]['id'] }
]
for teamName in teamNames:
    teams.append({'teamName': teamName})

request = urllib2.Request('%s/api/v1/releases/%s/teams' % (xlr_url, template['id']), json.dumps(teams), headers)
response = opener.open(request)

jythonResponse.statusCode = 200
jythonResponse.entity = json.dumps({"result": "Successfully imported template [%s]" % template_name})