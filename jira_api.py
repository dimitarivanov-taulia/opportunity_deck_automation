import re
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
    return ''.join(parsed_text)

def fetch_jira_data():
    url = "https://taulia.atlassian.net/rest/api/3/search"
    auth = HTTPBasicAuth("dimitar.ivanov@taulia.com", os.getenv('JIRA_API_KEY'))
    headers = {"Accept": "application/json"}

    # JQL query to fetch non-closed tickets with the specific Customer Request Type
    jql_query = 'project = DATA AND "Customer Request Type" = "Upsell/Expansion Opportunity Deck" AND status != Closed'
    # Specify the custom fields you want to retrieve
    params = {
        'jql': jql_query,
        'fields': 'summary,description,customfield_10840,customfield_21373,customfield_21375,customfield_21374,customfield_21372,customfield_21371,customfield_21370,customfield_21369,customfield_21368,customfield_21367',
        'maxResults': 50  # Adjust as needed
    }

    response = requests.get(url, headers=headers, params=params, auth=auth)
    if response.status_code != 200:
        print(f"Failed to retrieve data from Jira. Status code: {response.status_code}")
        print(f"Error message: {response.text}")
        return

    data = response.json()
    selected_issues = data.get('issues', [])

    if not selected_issues:
        print("No issues found matching the JQL query.")
        return

    issues_info = []
    for issue in selected_issues:
        fields = issue.get('fields', {})
        issue_info = {
            "Issue Key": issue.get("key"),
            "Buyer Company Name": fields.get("customfield_10840", [{}])[0].get("value"),
            "Summary": fields.get("summary"),
            "Description": parse_description(fields.get("description")),
            "Gross Discount Target": fields.get("customfield_21373"),
            "Blended Rate APR": fields.get("customfield_21375"),
            "Buyer APR Floor": str(int(fields.get("customfield_21374"))),
            "Target Term": fields.get("customfield_21372"),
            "Working Capital Goal": fields.get("customfield_21371"),
            "Products we’re selling": fields.get("customfield_21370", [{}])[0].get("value"),
            "Opportunity Type": fields.get("customfield_21369", {}).get("value"),
            "Current Program Performance": fields.get("customfield_21368", {}).get("value"),
            "Current Products": [product.get("value") for product in fields.get("customfield_21367", [])],
        }
        # Remove None values
        issue_info = {k: v for k, v in issue_info.items() if v is not None}
        issues_info.append(issue_info)

        #Map Funding Options
        if issue_info['Opportunity Type'] == "Upsell" and "DD" in issue_info['Current Products']:
            issue_info["Funding Options"] = "DD Only"
        elif issue_info['Opportunity Type'] == "Upsell" and "SCF" in issue_info['Current Products']:
            issue_info["Funding Options"] = "SCF+ Only"
        else:
            issue_info["Funding Options"] = "Flexible Funding"

        #Map Spend file descritpiton:
        pattern = r"(\S+_custom_\d+)|(\S+_spend_\d+)"
        spend_file = re.search(pattern, issue_info['Description'], flags=0)
        if spend_file is None:
            issue_info["Spend File"] = "LIVE Data"
        else:
            issue_info["Spend File"] = spend_file.group()

    # Save the issues information in JSON format to a file
    with open('issues_info.json', 'w') as json_file:
        json.dump(issues_info, json_file, indent=4)

    print("Issues information saved to issues_info.json")

fetch_jira_data()
