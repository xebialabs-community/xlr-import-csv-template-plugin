#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import csv, json
from java.util import Date
from sets import Set

from com.xebialabs.xlrelease.domain import Release
from com.xebialabs.xlrelease.domain.status import ReleaseStatus
from com.xebialabs.xlrelease.api.v1.views import TeamView

field_to_column_index_mapping = {
    'phase_name': 0,
    'title': 1,
    'description': 5,
    'team': 6
}

phase_name_id_map = {}


def create_team(teamName, id=None):
    teamView = TeamView()
    teamView.id = id
    teamView.teamName = teamName
    return teamView

def add_teams_to_template(template, tasks):
    unique_teams = Set([task['team'] for task in tasks])
    unique_teams.remove('')

    teams = []
    for team in template['teams']:
        teams.append(create_team(team['teamName'], team.id))

    for team_name in unique_teams:
        teams.append(create_team(team_name))

    templateApi.setTeams(template.id, teams)

def add_phase_if_not_exists_and_return_id(template, phase_name):
    if phase_name not in phase_name_id_map.keys():
        phase = phaseApi.addPhase(template.id, phaseApi.newPhase(phase_name))
        phase_name_id_map[phase_name] = phase.id

    return phase_name_id_map[phase_name]

def parse_csv(csv_str):
    parsed_tasks = []
    template_reader = csv.reader(csv_str.split('\n'), delimiter='\t', dialect='excel', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in template_reader:
        if len(row) < max(field_to_column_index_mapping.values()):
            logger.warn('Skipping row [%s] due to too little columns' % row)
            continue

        task = {}
        task['phase_name'] = row[field_to_column_index_mapping['phase_name']]
        task['title'] = row[field_to_column_index_mapping['title']]
        task['description'] = row[field_to_column_index_mapping['description']]
        task['team'] = row[field_to_column_index_mapping['team']]
        
        parsed_tasks.append(task)

    return parsed_tasks

def add_tasks_to_template(template, tasks):
    for task in tasks:
        phase_name = task['phase_name']
        title = task['title']
        description = task['description']
        team = task['team']
        
        phase_id = add_phase_if_not_exists_and_return_id(template, phase_name)

        task = taskApi.newTask()
        task.description = description
        task.title = title

        if team:
            task.team = team

        phaseApi.addTask(phase_id, task, None)

def create_blank_template(template_name):
    template = Release()
    template.title = template_name
    template.status = ReleaseStatus.TEMPLATE
    template.scheduledStartDate = Date()
    template.dueDate = Date(template.scheduledStartDate.getTime() + 3600000)
    template = templateApi.createTemplate(template)

    # Delete unnecessary "New Phase"
    phaseApi.deletePhase(template['phases'][0].id)

    return template






for item in request.entity:
    if item['name'] == 'csv':
        csv_str = str(item['value'])
    if item['name'] == 'template_name':
        template_name = item['value']

try: 
    template = create_blank_template(template_name)
    tasks = parse_csv(csv_str)
    add_tasks_to_template(template, tasks)
    add_teams_to_template(template, tasks)

    response.statusCode = 200
    response.entity = {
        "id": template.id,
        "message": "Successfully imported template [%s]" % template_name
    }

except (RuntimeError, TypeError, NameError) as e:
    logger.error("Unexpected error:", str(e))

    response.statusCode = 500
    response.entity = json.dumps({"result": "Error importing template [%s]" % str(e)})

