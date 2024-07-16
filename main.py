#TODO Run file by file when done
import looker_sdk
from looker_sdk import models40

# Initialize Looker SDK
sdk = looker_sdk.init40("looker_na.ini")

# Define dashboard dictionary with names (LookML dashboards)
dashboards_dict = {
    'payables_benchmark::buyer__payables_benchmark': ['Peer DPO', 'Card Adoption', 'Supplier Payment Terms Comparison'],
    '165': ['Top WC Potential Suppliers', 'Working Capital Released', 'Industry Term Comparison'],
    'payables_planner::buyer__payables_planner_supplier_list': ['Buyer - Payables Planner Supplier List',]

}

# Get all dashboards
dashboards = sdk.all_dashboards()

# Collect dashboard information
dashboard_info = [(db.id, db.title) for db in dashboards]

# Iterate through each dashboard
for id, dashboard_name in dashboard_info:
    # Debug print to check IDs
    # print(f"Checking dashboard: {id} - {dashboard_name}")
    if id in dashboards_dict.keys():
        print(f"Found matching dashboard: {id} - {dashboard_name}")

        # Get dashboard elements
        try:
            # For LookML dashboards, we need to use the dashboard ID correctly
            dashboard = sdk.dashboard(id)
            dashboard_elements = dashboard.dashboard_elements
            print(f"Number of elements found: {len(dashboard_elements)}")
            for element in dashboard_elements:
                if element.title in dashboards_dict[id]:
                    print(f"Element title: {element.title}")
        except looker_sdk.error.SDKError as e:
            print(f"Error fetching dashboard elements for {id}: {e}")
