import json
import subprocess
import os

# Define dashboard dictionary with names (LookML dashboards)
DASHBOARD_DICT = {
    'payables_benchmark::buyer__payables_benchmark': ['Peer DPO', 'Card Adoption', 'Supplier Payment Terms Comparison'],
    '165': ['Top WC Potential Suppliers', 'Working Capital Released', 'Industry Term Comparison'],
    'payables_planner::buyer__payables_planner_supplier_list': ['Buyer - Payables Planner Supplier List'],
}


def run_script(script_name):
    process = subprocess.Popen(
        ["python", script_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    for line in process.stdout:
        print(line, end="")

    stderr = process.communicate()[1]
    if process.returncode != 0:
        print(f"Error running {script_name}: {stderr}")
        exit(1)
    else:
        print(f"Completed running {script_name}")


def main():
    # Step 1: Run jira_api to generate filter_update dict
    print("Running jira_api.py...")
    run_script("jira_api.py")

    # Validate that the issues_info.json file was created and contains data
    if not os.path.exists('issues_info.json'):
        print("issues_info.json file not found. Exiting.")
        exit(1)

    with open('issues_info.json', 'r') as json_file:
        issues_info = json.load(json_file)

    if not issues_info:
        print("No issue info available. Exiting.")
        exit(1)

    # Assuming we're working with the first issue in the list for now
    first_issue = issues_info[0]
    GLOBAL_BUYER_NAME = first_issue.get("Buyer Company Name")
    FILTER_UPDATES = first_issue

    if not GLOBAL_BUYER_NAME:
        print("Buyer Company Name not found in issue info. Exiting.")
        exit(1)

    print(f"GLOBAL_BUYER_NAME set to: {GLOBAL_BUYER_NAME}")
    print(f"FILTER_UPDATES set to: {FILTER_UPDATES}")

    # Set environment variables for the subprocesses if needed
    os.environ["GLOBAL_BUYER_NAME"] = GLOBAL_BUYER_NAME
    os.environ["FILTER_UPDATES"] = json.dumps(FILTER_UPDATES)
    os.environ["DASHBOARD_DICT"] = json.dumps(DASHBOARD_DICT)

    # Step 2: Run tile_render to render the required tiles
    print("Running tile_render.py...")
    run_script("tile_render.py")

    # Step 3: Run data_fetch to fetch the required data
    print("Running data_fetch.py...")
    run_script("data_fetch.py")

    # Step 4: Run presentation_generator to generate the final presentation
    print("Running presentation_generator.py...")
    run_script("presentation_generator.py")


if __name__ == "__main__":
    main()
