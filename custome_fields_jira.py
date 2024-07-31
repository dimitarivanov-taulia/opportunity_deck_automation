import json
import looker_sdk
from looker_sdk import models40

# Initialize Looker SDK
sdk = looker_sdk.init40("looker.ini")

# Define dashboard dictionary with names (LookML dashboards and UDDs)
dashboards_dict = {
    'payables_benchmark::buyer__payables_benchmark': ['Card Adoption',]# 'Supplier Payment Terms Comparison'],
    # '165': ['Top WC Potential Suppliers', 'Working Capital Released', 'Industry Term Comparison'],
    # 'payables_planner::buyer__payables_planner_supplier_list': ['Buyer - Payables Planner Supplier List'],
}

# Define filter updates as given
filter_updates = {
    "Buyer Company Name": "AcmeBirdSeed",
    "Scenario Description": "Harmonized terms",
    "Spend File": 'AcmeBirdSeed_spend_022024',
}

# Map filter names to database column names for each element
filter_mappings = {
    'Peer DPO': {
        "Buyer Company Name": "capiq_peer_v2.peer_company_name",
        "Scenario Description": "scenario_description",
        "Spend File": "file_source_description",
    },
    'Card Adoption': {
        "Buyer Company Name": "consolidated_buyer_name",
        "Scenario Description": "scenario_description",
        "Spend File": "file_source_description",
    },
    'Supplier Payment Terms Comparison': {
        "Buyer Company Name": "buyer_name",
        "Scenario Description": "scenario_description",
        "Spend File": "file_source_description",
    },
    # Add similar mappings for other elements as needed
}

class LookerDashboardManager:
    def __init__(self, sdk):
        self.sdk = sdk

    def run_inline_query_with_extra_filters(self, model, view, fields, filters={}, with_filters=True, filter_mapping=None):
        # Map the filters using filter_mapping
        mapped_filters = {filter_mapping[k]: v for k, v in filters.items()} if with_filters and filter_mapping else {}

        # Add filter fields to the query fields to ensure they are included in the results
        filter_fields = list(mapped_filters.keys())
        all_fields = list(set(fields + filter_fields))

        query_payload = {
            'model': model,
            'view': view,
            'fields': all_fields,
            'filters': mapped_filters,
            'limit': '500'
        }

        filter_status = "with filters" if with_filters else "without filters"
        print(f"Running query {filter_status} with payload:")
        print(json.dumps(query_payload, indent=2))

        try:
            run_query_response = self.sdk.run_inline_query(
                result_format='json', body=models40.WriteQuery(**query_payload))
            run_query_look_data = json.loads(run_query_response)  # Parse the JSON response
            print(f"Result {filter_status} >> " + json.dumps(run_query_look_data, indent=2))
            return run_query_look_data
        except looker_sdk.error.SDKError as e:
            print(f"Error running query {filter_status}: {e}")
            return None

    def export_looks_from_dashboard(self, dashboard_id, is_lookml_dashboard=False):
        dashboard_elements = self.fetch_dashboard_elements(dashboard_id, is_lookml_dashboard)
        if not dashboard_elements:
            print(f"No elements found for dashboard ID: {dashboard_id}")
            return

        # Get the list of elements to export for this dashboard
        elements_to_export = dashboards_dict.get(dashboard_id, [])

        for element in dashboard_elements:
            if element.title in elements_to_export and element.result_maker:
                try:
                    query = element.result_maker.query
                    print(f"Processing result_maker for element: {element.title}")

                    # Dynamically retrieve model, view, and fields from the query
                    model = query.model
                    view = query.view
                    fields = query.fields

                    # Retrieve the specific filter mapping for the element
                    filter_mapping = filter_mappings.get(element.title, {})

                    # Run query without filters
                    print(f"\nQuery results for element '{element.title}' without filters:")
                    query_results_no_filters = self.run_inline_query_with_extra_filters(model, view, fields, filter_updates, with_filters=False)

                    # Run query with filters
                    print(f"\nQuery results for element '{element.title}' with filters:")
                    query_results_with_filters = self.run_inline_query_with_extra_filters(model, view, fields, filter_updates, with_filters=True, filter_mapping=filter_mapping)

                    # Debugging: Ensure results contain expected fields
                    if query_results_with_filters:
                        print(f"Fields in filtered results: {query_results_with_filters[0].keys()}")
                    else:
                        print("No results returned for filtered query.")

                    # Save filtered results with filters if they exist
                    if query_results_with_filters:
                        csv_file = f"data/{element.title}_with_filters.csv"
                        with open(csv_file, "w") as fh:
                            json.dump(query_results_with_filters, fh)
                            print(f"Saved {csv_file}")
                    else:
                        print(f"No data returned for {element.title} with filters")

                    # Save results without filters if they exist
                    if query_results_no_filters:
                        csv_file_no_filters = f"data/{element.title}_without_filters.csv"
                        with open(csv_file_no_filters, "w") as fh:
                            json.dump(query_results_no_filters, fh)
                            print(f"Saved {csv_file_no_filters}")
                    else:
                        print(f"No data returned for {element.title} without filters")
                except looker_sdk.error.SDKError as e:
                    print(f"Error processing result_maker for element {element.title}: {e}")

    def fetch_dashboard_elements(self, dashboard_id, is_lookml_dashboard=False):
        print(f"Fetching elements for dashboard ID '{dashboard_id}'")
        try:
            dashboard = self.sdk.dashboard(dashboard_id=dashboard_id)
            dashboard_elements = dashboard.dashboard_elements

            if not dashboard_elements:
                print(f"No elements found for dashboard ID '{dashboard_id}'")
            else:
                element_titles = [element.title for element in dashboard_elements]
                print(f"Elements in dashboard ID '{dashboard_id}': {element_titles}")
            return dashboard_elements
        except looker_sdk.error.SDKError as e:
            print(f"Error fetching elements for dashboard ID '{dashboard_id}': {e}")
            return []

    def sync_dashboard(self, dash_id):
        print(f"Processing dashboard '{dash_id}'")
        is_lookml_dashboard = "::" in dash_id  # Determine if it is a LookML dashboard
        self.export_looks_from_dashboard(dash_id, is_lookml_dashboard)

    def sync_all_dashboards(self):
        for dash_id in dashboards_dict.keys():
            self.sync_dashboard(dash_id)

# Create an instance of the LookerDashboardManager
manager = LookerDashboardManager(sdk)

# Sync all dashboards
manager.sync_all_dashboards()
