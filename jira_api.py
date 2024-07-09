import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

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
            if field_data:
                request_type_name = field_data['requestType']
                if request_type_name == "Upsell/Expansion Opportunity Deck":
                    issue_key = issue['key']
                    summary = issue['fields'].get('summary', '')
                    current_status = field_data['currentStatus']['status']

                    # Hypothetical paths to the form data
                    form_data = field_data.get('formData', {})
                    print(form_data)

                    product_usage = field_data.get('formData', {}).get('productUsage', [])
                    performance = field_data.get('formData', {}).get('performance', '')

                    issues_dict[issue_key] = {
                        'Summary': summary,
                        'Request Type': request_type_name,
                        'Current Status': current_status,
                        'Product Usage': product_usage,
                        'Performance': performance
                    }

        for key, value in issues_dict.items():
            print(f"Issue Key: {key}, Details: {value}")
    else:
        print(f"Failed to retrieve data from Jira. Status code: {response.status_code}")
        print(f"Error message: {response.text}")

fetch_jira_data()

#"customfield_10840":[{"self":"https://taulia.atlassian.net/rest/api/3/customFieldOption/16712","value":"American Water","id":"16712"}]