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
from java.util import Date
from sets import Set

from com.xebialabs.xlrelease.domain import Release
from com.xebialabs.xlrelease.domain.status import ReleaseStatus
from com.xebialabs.xlrelease.api.v1.views import TeamView

def create_team(teamName, id=None):
    teamView = TeamView()
    teamView.id = id
    teamView.teamName = teamName
    return teamView

def add_teams_to_template(template, teamNames):
    teams = []
    teams.append(create_team(template['teams'][0]['teamName'], template['teams'][0].id))
    teams.append(create_team(template['teams'][1]['teamName'], template['teams'][1].id))

    for teamName in teamNames:
        teams.append(create_team(teamName))

    templateApi.setTeams(template.id, teams)

for item in request.entity:
    if item['name'] == 'csv':
        csv_str = str(item['value'])
    if item['name'] == 'template_name':
        template_name = item['value']

try: 
    template = Release()
    template.title = template_name
    template.status = ReleaseStatus.TEMPLATE
    template.scheduledStartDate = Date()
    template.dueDate = Date(template.scheduledStartDate.getTime() + 3600000)
    template = templateApi.createTemplate(template)

    # Delete unnecessary "New Phase"
    phaseApi.deletePhase(template['phases'][0].id)

    phases = []
    phase_name_id_map = {}
    template_reader = csv.reader(csv_str.split('\n'), delimiter='\t', dialect='excel', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in template_reader:
        if not row[0] in phases:
            phase_name = row[0]
            phases.append(phase_name)
            phase = phaseApi.addPhase(template.id, phaseApi.newPhase(phase_name))
            phase_name_id_map[phase_name] = phase.id

    # Create Tasks
    teamNames = Set([])
    template_reader = csv.reader(csv_str.split('\n'), delimiter='\t', dialect='excel', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in template_reader:
        phase_id = phase_name_id_map[row[0]]
        title = row[1]
        description = row[5]
        team = row[6]

        task = taskApi.newTask()
        task.description = description
        task.title = title

        if team:
            task.team = team
            teamNames.add(team)

        phaseApi.addTask(phase_id, task, None)

    add_teams_to_template(template, teamNames)

    response.statusCode = 200
    response.entity = json.dumps({"result": "Successfully imported template [%s]" % template_name})

except (RuntimeError, TypeError, NameError) as e:
    print("Unexpected error:", str(e))

    response.statusCode = 500
    response.entity = json.dumps({"result": "Error importing template [%s]" % str(e)})

