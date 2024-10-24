from jira import JIRA
import os
import requests
import datetime
from enum import Enum
from flask import Blueprint, request, make_response, jsonify
from config import *
import base64
from werkzeug.utils import secure_filename
from mimetypes import guess_extension
import mimetypes


jira = JIRA(server=JIRA_CRED['server'],token_auth=JIRA_CRED['token'])

class IssueType(Enum):
    BUG = "Bug"
    FEATURE = "Story"
    SUPPORT = "Task"
    TASK = "Task"
    STORY = "Story"
    EPIC = "Epic"
    ISSUE = "Task"

class Priority(Enum):
    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOWEST = "Lowest"
def parse_attachment(file_data, file_name, folder_this):
    """ Save attachment to bucket/chat_id folder and return base64 encoded content. """
    chat_folder = os.path.join(folder_this)
    os.makedirs(chat_folder, exist_ok=True)
    file_path = os.path.join(folder_this, file_name)

    # Write the file to disk
    with open(file_path, "wb") as f:
        f.write(file_data)

    # Convert file to base64
    with open(file_path, "rb") as f:
        file_ext = file_path.split('.')[-1]
        mime_type = guess_extension(file_ext) or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        
    return file_name, mime_type,file_path

    

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
    def process_attachment(self,key,incomming_attachment):
        # print(attachments)
        attachments = []
        for attachment in incomming_attachment:
            if attachment:
                # print(f"Attachment {filename} has been added to issue {key}. File Path: {file_path}")
                b_file_data = base64.b64decode(attachment['data'])
                filePaththis = ticket_folder
                print(filePaththis)
                filename, mime, file_path = parse_attachment(b_file_data, secure_filename(attachment['name']), filePaththis)
                return self.add_attachment(key, file_path)

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

    def geturlfromIssue(self,issue_key):
        issue = self.jira.issue(issue_key)
        return issue.permalink()
jira_integration = JiraIntegration(jira)
jiraint=Blueprint('jira',__name__)
@jiraint.route('/get_projects',methods=['GET'])
def get_projects():
    return jira_integration.get_projects()
@jiraint.route('/create_issue',methods=['POST'])
def create_issue():
    print(request.json)
    project = request.json.get('project', 'NULL')
    summary = request.json.get('subject', '')
    description = f"{request.json.get('summary', '')}\n{request.json.get('description', '')}"
    issuetype = IssueType[request.json.get('issue_type', 'TASK').upper() if request.json.get('issue_type') else 'TASK']
    priority = Priority[request.json.get('priority', 'LOWEST').upper() if request.json.get('priority') else 'LOWEST']
    issue = jira_integration.create_issue(project, summary, description, issuetype, priority)
    assignee = request.json.get('assignee', '')
    reporter = request.json.get('reporter', '')
    attachment = request.json.get('attachments')
    if attachment:
        jira_integration.process_attachment(issue.key, attachment)
    if assignee:
        jira_integration.assign_issue(issue.key, assignee=assignee)
    if reporter:
        jira_integration.assign_issue(issue.key, reporter=reporter)
    url=jira_integration.geturlfromIssue(issue.key)
    # redirect(url)
    return make_response(jsonify({'issue_key': issue.key,'url':url}), 200)
@jiraint.get('/get_similar_issues')
def get_similar_issues():
    keyword = request.args.get('keyword')
    issues = jira_integration.search_similar_issues(keyword)
    data = []
    for x in issues[:10]:
        data.append(jira_integration.get_content(x[0]))
    return data
@jiraint.get('/get_content')
def get_content():
    issue_key = request.args.get('issue_key')
    return jira_integration.get_content(issue_key)

# print("\nTest 1: Getting Projects:")
# print(jira_integration.get_projects())

# print("\nTest 2: Creating Issue:")
# project = input("Enter the project key: ")
# summary = input("Enter the issue summary: ")
# description = input("Enter the issue description: ")
# issuetype_input = input("Enter the issue type (Bug, Task, Story, Epic): ")
# issuetype = IssueType[issuetype_input.upper()]
# priority_input = input("Enter the priority (Highest, High, Medium, Low, Lowest): ")
# priority = Priority[priority_input.upper()]

# issue = jira_integration.create_issue(project, summary, description, issuetype, priority)
# print(f"Issue created: {issue}")

# print("\nTest 3: Assign Issue:")
# result = jira_integration.assign_issue(issue.key, assignee='akileswar')
# print(result)

# print("\nTest 4: Assign Reporter:")
# result = jira_integration.assign_issue(issue.key, reporter='akileswar')
# print(result)

# print("\nTest 5: Add Attachments from URL:")
# attachment_result = jira_integration.add_attachment(issue.key, 'https://cloudinary-marketing-res.cloudinary.com/images/w_1000,c_scale/v1679921049/Image_URL_header/Image_URL_header-png?_i=AA')
# print(attachment_result)

# print("\nTest 6: Add Attachments from File:")
# attachment_result = jira_integration.add_attachment(issue.key, './dockerfile')
# print(attachment_result)

# print("\nTest 7: Get Attachments from Issue:")
# jira_integration.get_attachment(issue.key)

# print("\nTest 8: Get Contents from Issue:")
# print(jira_integration.get_content(issue.key))

# print("Test 9: Search Similar Issues")
# results = jira_integration.search_similar_issues(input("Enter search Key: "))
# for result in results:
#     print(f"{result}")


