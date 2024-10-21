from jira import JIRA
import os
import requests
import datetime
from enum import Enum
#from config import *
JIRA_CRED = dict({
    'token':  os.getenv("JIRA_SERVER_token", 'http://34.132.196.121:8080')
    'server': os.getenv("JIRA_SERVER", 'http://34.132.196.121:8080')
})
jira = JIRA(server=JIRA_CRED['server'],token_auth=JIRA_CRED['token'])

class IssueType(Enum):
    BUG = "Bug"
    TASK = "Task"
    STORY = "Story"
    EPIC = "Epic"

class Priority(Enum):
    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOWEST = "Lowest"

class JiraIntegration:
    def __init__(self, jira):
        self.jira = jira

    def get_projects(self):
        projects = self.jira.projects()
        return [project.key for project in projects]

    def assign_issue(self, issue: str, assignee: str = None, reporter: str = None):
        issue_obj = self.jira.issue(issue)
        response_message = f"Issue {issue} has been updated."
        
        if assignee:
            self.jira.assign_issue(issue_obj, assignee)
            response_message += f" Assigned to {assignee}."
        
        if reporter:
            issue_obj.update(fields={'reporter': {'name': reporter}})
            response_message += f" Reporter set to {reporter}."
        
        return response_message

    def create_issue(self, project: str, summary: str, description: str, issuetype: IssueType, priority: Priority = Priority.LOWEST):
        issue_dict = {
            'project': {'key': project},
            'summary': summary,
            'description': description,
            'priority': {'name': priority.value},
            'issuetype': {'name': issuetype.value},
        }
        
        new_issue = self.jira.create_issue(fields=issue_dict)
        return new_issue
    
    def add_attachment(self, issue_key: str, attachment_path: str):
        issue = self.jira.issue(issue_key)
        if os.path.isfile(attachment_path):
            self.jira.add_attachment(issue=issue, attachment=attachment_path)
            return f"Attachment {attachment_path} has been added to issue {issue_key}."
        elif attachment_path.startswith(('http://','https://')):
            response = requests.get(attachment_path)
            if response.status_code == 200:
                attachment_name = os.path.basename(attachment_path)
                temp_file_path = f"/tmp/attachment_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(response.content)
                self.jira.add_attachment(issue=issue, attachment=temp_file_path)
                os.remove(temp_file_path)
                return f"Attachment {temp_file_path} has been added to issue {issue_key}."
    
    def get_attachment(self, issue_key: str):
        issue = self.jira.issue(issue_key)
        for attachment in issue.fields.attachment:
            print("Name: '{filename}', size: {size}".format(
                filename=attachment.filename, size=attachment.size))

    def get_content(self, issue_key: str):
        obj = self.jira.issue(issue_key)
        res = {
            'key': obj.key,
            'summary': obj.fields.summary,
            'description': obj.fields.description,
            'issuetype': obj.fields.issuetype.name,
            'status': obj.fields.status.name,
            'assignee': obj.fields.assignee.displayName if obj.fields.assignee else None,
            'reporter': obj.fields.reporter.displayName if obj.fields.reporter else None,
            'created': obj.fields.created,
            'updated': obj.fields.updated,
            'attachments': [{'filename': attachment.filename, 'size': attachment.size} for attachment in obj.fields.attachment]
        }
        return res

    def search_similar_issues(self, keyword: str):
        jql_query = f'text ~ "{keyword}" ORDER BY created DESC'
        issues = self.jira.search_issues(jql_query, maxResults=5)
        return [(issue.key, issue.fields.summary) for issue in issues]

jira_integration = JiraIntegration(jira)

print("\nTest 1: Getting Projects:")
print(jira_integration.get_projects())

print("\nTest 2: Creating Issue:")
project = input("Enter the project key: ")
summary = input("Enter the issue summary: ")
description = input("Enter the issue description: ")
issuetype_input = input("Enter the issue type (Bug, Task, Story, Epic): ")
issuetype = IssueType[issuetype_input.upper()]
priority_input = input("Enter the priority (Highest, High, Medium, Low, Lowest): ")
priority = Priority[priority_input.upper()]

issue = jira_integration.create_issue(project, summary, description, issuetype, priority)
print(f"Issue created: {issue}")

print("\nTest 3: Assign Issue:")
result = jira_integration.assign_issue(issue.key, assignee='akileswar')
print(result)

print("\nTest 4: Assign Reporter:")
result = jira_integration.assign_issue(issue.key, reporter='rajashree')
print(result)

print("\nTest 5: Add Attachments from URL:")
attachment_result = jira_integration.add_attachment(issue.key, 'https://cloudinary-marketing-res.cloudinary.com/images/w_1000,c_scale/v1679921049/Image_URL_header/Image_URL_header-png?_i=AA')
print(attachment_result)

print("\nTest 6: Add Attachments from File:")
attachment_result = jira_integration.add_attachment(issue.key, './dockerfile')
print(attachment_result)

print("\nTest 7: Get Attachments from Issue:")
jira_integration.get_attachment(issue.key)

print("\nTest 8: Get Contents from Issue:")
print(jira_integration.get_content(issue.key))

print("Test 9: Search Similar Issues")
results = jira_integration.search_similar_issues(input("Enter search Key: "))
for result in results:
    print(f"{result}")
