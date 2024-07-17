import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json

load_dotenv()


def parse_description(description):
    """Parse the description content if it's in the Jira document format."""
    if not description or 'content' not in description:
        return ""

    parsed_text = []
    for block in description['content']:
        if block['type'] == 'paragraph':
            for content in block.get('content', []):
                if content['type'] == 'text':
                    parsed_text.append(content['text'])
                elif content['type'] == 'inlineCard':
                    parsed_text.append(content['attrs']['url'])
        parsed_text.append('\n')
    return ''.join(parsed_text)


def fetch_jira_data():
    url = "https://taulia.atlassian.net/rest/api/3/search"
    auth = HTTPBasicAuth("dimitar.ivanov@taulia.com", os.getenv('JIRA_API_KEY'))
    headers = {"Accept": "application/json"}

    jql_query = 'project = DATA AND "Customer Request Type" = "Upsell/Expansion Opportunity Deck"'
    params = {'jql': jql_query,
              'fields': 'summary,description,customfield_13140,issuetype,status,priority,created,updated,attachment,comment'}

    response = requests.get(url, headers=headers, params=params, auth=auth)
    if response.status_code != 200:
        print(f"Failed to retrieve data from Jira. Status code: {response.status_code}")
        print(f"Error message: {response.text}")
        return

    data = response.json()
    print("Response Data: ", json.dumps(data, indent=2))

    selected_issues = data.get('issues', [])
    if not selected_issues:
        print("No issues found matching the JQL query.")
        return

    issues_dict = {}
    for issue in selected_issues:
        fields = issue.get('fields', {})
        if not fields:
            print(f"No fields found for issue: {issue['key']}")
            continue

        issue_key = issue['key']
        summary = fields.get('summary', '')
        description = parse_description(fields.get('description', ''))
        customfield_13140 = fields.get('customfield_13140', {})

        request_type_name = customfield_13140.get('requestType', {}).get('name', '')
        issue_type = fields.get('issuetype', {}).get('name', '')
        status = fields.get('status', {}).get('name', '')
        priority = fields.get('priority', {}).get('name', '')
        created = fields.get('created', '')
        updated = fields.get('updated', '')

        # Access attached forms
        attached_forms = get_attached_forms(issue_key)

        # Access attachments
        attachments = fields.get('attachment', [])
        attachment_info = [{'filename': attachment.get('filename', ''), 'content': attachment.get('content', '')} for
                           attachment in attachments]

        # Access comments
        comments = fields.get('comment', {}).get('comments', [])
        comment_info = [comment.get('body', '') for comment in comments]

        print(f"Issue Name: {summary}")  # Print only the issue name

        # Collect all fields
        issues_dict[issue_key] = {
            'Summary': summary,
            'Description': description,
            'Request Type': request_type_name,
            'Issue Type': issue_type,
            'Status': status,
            'Priority': priority,
            'Created': created,
            'Updated': updated,
            'Attached Forms': attached_forms,
            'Attachments': attachment_info,
            'Comments': comment_info,
            'All Fields': fields  # Store all fields
        }

    for key, value in issues_dict.items():
        print(f"Issue Key: {key}, Details: {value}")


def get_attached_forms(issue_key):
    url = f"https://taulia.atlassian.net/rest/servicedeskapi/request/{issue_key}/form"
    auth = HTTPBasicAuth("dimitar.ivanov@taulia.com", os.getenv('JIRA_API_KEY'))
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve form data: {response.status_code} - {response.text}")
        return None


fetch_jira_data()
