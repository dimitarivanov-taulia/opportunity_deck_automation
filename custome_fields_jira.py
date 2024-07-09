import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_jira_data():
    url = "https://taulia.atlassian.net/rest/api/3/search"
    auth = HTTPBasicAuth("dimitar.ivanov@taulia.com", os.getenv('JIRA_API_KEY'))  # Replace with your credentials
    headers = {"Accept": "application/json"}

    jql_query = 'project = DATA'

    params = {
        'jql': jql_query,
        'fields': 'summary,customfield_13140'  # Retrieves specific fields
    }

    response = requests.get(url, headers=headers, params=params, auth=auth)
    if response.status_code == 200:
        data = response.json()
        selected_issues = data['issues']

        issues_dict = {}

        for issue in selected_issues:
            field_data = issue['fields'].get('customfield_13140')
            print("Full field data for issue:", issue['key'])
            print(field_data)  # Debug print to show the full field_data content

            if field_data:
                request_type_name = field_data.get('requestType', {}).get('name')
                if request_type_name == "Upsell/Expansion Opportunity Deck":
                    issue_key = issue['key']
                    summary = issue['fields'].get('summary', '')
                    current_status = field_data.get('currentStatus', {}).get('status')

                    # Hypothetical paths to the form data (check all keys in field_data)
                    form_data = field_data.get('formData', {})
                    print(f"Form Data for issue {issue_key}: {form_data}")  # Debug print to show form data

                    product_usage = form_data.get('productUsage', [])
                    performance = form_data.get('performance', '')

                    issues_dict[issue_key] = {
                        'Summary': summary,
                        'Request Type': request_type_name,
                        'Current Status': current_status,
                        'Product Usage': product_usage,
                        'Performance': performance,
                        'Full Field Data': field_data  # Including full field data for further inspection
                    }

        for key, value in issues_dict.items():
            print(f"Issue Key: {key}, Details: {value}")
    else:
        print(f"Failed to retrieve data from Jira. Status code: {response.status_code}")
        print(f"Error message: {response.text}")

fetch_jira_data()
