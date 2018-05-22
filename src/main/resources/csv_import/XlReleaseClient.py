#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from java.util import Date
from sets import Set

from com.xebialabs.xlrelease.domain import Release
from com.xebialabs.xlrelease.domain.status import ReleaseStatus
from com.xebialabs.xlrelease.api.v1.views import TeamView

class XlReleaseClient:
    def __init__(self, templateApi, phaseApi, taskApi):
        self.phase_name_id_map = {}    
        self.templateApi = templateApi
        self.phaseApi = phaseApi
        self.taskApi = taskApi


    def create_team(self, teamName, id=None):
        teamView = TeamView()
        teamView.id = id
        teamView.teamName = teamName
        return teamView

    def add_teams_to_template(self, template, tasks):
        teams = []
        for team in template['teams']:
            teams.append(self.create_team(team['teamName'], team.id))

        unique_teams = Set([task['team'] for task in tasks])
        unique_teams.remove('')
        for team_name in unique_teams:
            teams.append(self.create_team(team_name))

        self.templateApi.setTeams(template.id, teams)

    def add_phase_if_not_exists_and_return_id(self, template, phase_name):
        if phase_name not in self.phase_name_id_map.keys():
            phase = self.phaseApi.addPhase(template.id, self.phaseApi.newPhase(phase_name))
            self.phase_name_id_map[phase_name] = phase.id

        return self.phase_name_id_map[phase_name]

    def add_tasks_to_template(self, template, tasks):
        for task in tasks:
            phase_name = task['phase_name']
            title = task['title']
            description = task['description']
            team = task['team']
            taskType = task['type']
            
            phase_id = self.add_phase_if_not_exists_and_return_id(template, phase_name)

            if taskType.lower() == "gate":
              task = self.taskApi.newTask("xlrelease.GateTask")
            else:
              task = self.taskApi.newTask()
            task.description = description
            task.title = title

            if team:
                task.team = team

            self.phaseApi.addTask(phase_id, task, None)

    def create_blank_template(self, template_name):
        template = Release()
        template.title = template_name
        template.status = ReleaseStatus.TEMPLATE
        # workaround for http://xebialabs.zendesk.com/agent/tickets/11419 affecting XLR 7.5 & 7.6
        template.setProperty("riskScore", "0")
        template.setProperty("totalRiskScore", "0")
        # end workaround
        template.scheduledStartDate = Date()
        template.dueDate = Date(template.scheduledStartDate.getTime() + 3600000)

        template = self.templateApi.createTemplate(template)

        # Delete unnecessary "New Phase"
        self.phaseApi.deletePhase(template['phases'][0].id)

        return template
