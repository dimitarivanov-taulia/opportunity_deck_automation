import json
import os
import looker_sdk
from looker_sdk import models40

# Load the issues information from the JSON file
with open('issues_info.json', 'r') as json_file:
    issues_info = json.load(json_file)

# Assuming we're working with the first issue in the list for now
first_issue = issues_info[0]
GLOBAL_BUYER_NAME = first_issue["Buyer Company Name"]
FILTER_UPDATES = first_issue

# Load the dashboard dictionary from environment variable
DASHBOARD_DICT = json.loads(os.getenv('DASHBOARD_DICT'))

# Initialize Looker SDK
sdk = looker_sdk.init40("looker_na.ini")

# Define global variables
GLOBAL_SPACE = "Dimitar Ivanov"

class LookerDashboardManager:
    def __init__(self, sdk):
        self.sdk = sdk

    def get_default_filter_values(self, dashboard_id):
        dashboard = self.sdk.dashboard(dashboard_id=dashboard_id)
        default_filters = {}
        for filter_item in dashboard.dashboard_filters:
            default_filters[filter_item.name] = filter_item.default_value or ""
        return default_filters

    def merge_filters(self, default_filters, user_filters):
        merged_filters = default_filters.copy()
        for key, value in user_filters.items():
            merged_filters[key] = value
        return merged_filters

    def run_inline_query_with_extra_filters(self, model, view, fields, filters={}, with_filters=True, filterable_fields=None, default_filters={}, limit=None, sorts=None):
        if with_filters and filterable_fields:
            mapped_filters = {f.field: filters[f.dashboard_filter_name] for f in filterable_fields if f.dashboard_filter_name in filters}
            print(f"Mapped Filters: {json.dumps(mapped_filters, indent=2)}")
        else:
            mapped_filters = {}

        merged_filters = {**default_filters, **mapped_filters}

        query_payload = {
            'model': model,
            'view': view,
            'fields': fields,
            'filters': merged_filters,
            'limit': limit if limit else '500',
            'sorts': sorts
        }

        filter_status = "with filters" if with_filters else "without filters"
        print(f"Running query {filter_status} with payload:")
        print(json.dumps(query_payload, indent=2))

        try:
            run_query_response = self.sdk.run_inline_query(
                result_format='json', body=models40.WriteQuery(**query_payload))
            run_query_look_data = json.loads(run_query_response)

            sql_query = self.sdk.run_inline_query(
                result_format='sql', body=models40.WriteQuery(**query_payload))
            print(f"SQL Query {filter_status}: {sql_query}")

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

        elements_to_export = DASHBOARD_DICT.get(dashboard_id, [])

        for element in dashboard_elements:
            if element.title in elements_to_export and element.result_maker:
                try:
                    query = element.result_maker.query
                    filterable_fields = [listen for filterable in element.result_maker.filterables for listen in filterable.listen]

                    print(f"Processing result_maker for element: {element.title}")

                    model = query.model
                    view = query.view
                    fields = query.fields
                    limit = query.limit
                    sorts = query.sorts

                    default_query_filters = query.filters or {}
                    default_dashboard_filters = self.get_default_filter_values(dashboard_id)
                    all_default_filters = {**default_dashboard_filters, **default_query_filters}
                    print(f"Default Filters: {json.dumps(all_default_filters, indent=2)}")

                    merged_filters = self.merge_filters(all_default_filters, FILTER_UPDATES)
                    print(f"Merged Filters: {json.dumps(merged_filters, indent=2)}")

                    # Commenting out the part where the query runs without filters
                    # print(f"\nQuery results for element '{element.title}' without filters:")
                    # query_results_no_filters = self.run_inline_query_with_extra_filters(model, view, fields, {}, with_filters=False)

                    print(f"\nQuery results for element '{element.title}' with filters:")
                    query_results_with_filters = self.run_inline_query_with_extra_filters(model, view, fields, merged_filters, with_filters=True, filterable_fields=filterable_fields, default_filters=default_query_filters, limit=limit, sorts=sorts)

                    if query_results_with_filters:
                        print(f"Fields in filtered results: {query_results_with_filters[0].keys()}")
                    else:
                        print("No results returned for filtered query.")

                    filtered_results = [
                        {k: v for k, v in result.items() if k in fields}
                        for result in query_results_with_filters
                    ]

                    print(f"Filtered results: {json.dumps(filtered_results, indent=2)}")

                    if filtered_results:
                        csv_file = f"data/{element.title}_with_filters.csv"
                        with open(csv_file, "w") as fh:
                            json.dump(filtered_results, fh)
                            print(f"Saved {csv_file}")
                    else:
                        print(f"No data returned for {element.title} with filters")

                    # Commenting out the part where the results without filters are saved
                    # if query_results_no_filters:
                    #     csv_file_no_filters = f"data/{element.title}_without_filters.csv"
                    #     with open(csv_file_no_filters, "w") as fh:
                    #         json.dump(query_results_no_filters, fh)
                    #         print(f"Saved {csv_file_no_filters}")
                    # else:
                    #     print(f"No data returned for {element.title} without filters")
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
        is_lookml_dashboard = "::" in dash_id
        self.export_looks_from_dashboard(dash_id, is_lookml_dashboard)

    def sync_all_dashboards(self):
        for dash_id in DASHBOARD_DICT.keys():
            self.sync_dashboard(dash_id)

# Create an instance of the LookerDashboardManager
manager = LookerDashboardManager(sdk)

# Sync all dashboards
manager.sync_all_dashboards()