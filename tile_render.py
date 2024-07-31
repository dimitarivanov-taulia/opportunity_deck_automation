import json
import os
import time
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

    def get_folder_id(self, name):
        response = self.sdk.search_folders(name=name)
        if not response:
            raise Exception(f"Folder with name '{name}' not found.")
        return response[0].id

    def sync_lookml_to_udd(self, lookml_dash_id, udd_title):
        folder_id = self.get_folder_id(GLOBAL_SPACE)
        print(f"Folder ID for space '{GLOBAL_SPACE}': {folder_id}")

        existing_udds = self.sdk.search_dashboards(folder_id=folder_id, title=udd_title)

        body = models40.WriteDashboard(title=udd_title, crossfilter_enabled=True)

        print(f"syncing lookML dashboard '{udd_title}' to UDD...")
        if existing_udds is None or len(existing_udds) == 0:
            print(f"Importing LookML dashboard with ID '{lookml_dash_id}' to space ID '{folder_id}'")
            udd = self.sdk.import_lookml_dashboard(lookml_dashboard_id=lookml_dash_id,
                                                   space_id=folder_id,
                                                   body=body)
        else:
            print(f"Synchronizing existing UDD with LookML dashboard ID '{lookml_dash_id}'")
            self.sdk.sync_lookml_dashboard(lookml_dashboard_id=lookml_dash_id,
                                           body=body)
            udd = existing_udds[0]
        return self.sdk.update_dashboard(str(udd.id), body)

    def copy_non_lookml_dashboard(self, dashboard_id, udd_title):
        folder_id = self.get_folder_id(GLOBAL_SPACE)
        print(f"Folder ID for space '{GLOBAL_SPACE}': {folder_id}")

        print(f"Copying non-LookML dashboard with ID '{dashboard_id}' to space ID '{folder_id}'")
        new_dashboard = self.sdk.copy_dashboard(dashboard_id, folder_id)
        new_dashboard_id = new_dashboard.id

        # Update the title of the copied dashboard
        body = models40.WriteDashboard(title=udd_title)
        updated_dashboard = self.sdk.update_dashboard(new_dashboard_id, body)

        return updated_dashboard

    def generate_space(self, name):
        if not self.sdk.search_folders(name=name):
            folder = models40.CreateFolder(parent_id=1, name=name)
            self.sdk.create_folder(folder)

    def sync_all_dashboards(self):
        for dash_id in DASHBOARD_DICT.keys():
            try:
                dashboard = self.sdk.dashboard(dash_id)
                buyer_name = GLOBAL_BUYER_NAME if GLOBAL_BUYER_NAME is not None else "Unknown"
                dashboard_title = f"{dashboard.title} - {buyer_name}"
                self.generate_space(GLOBAL_SPACE)
                if '::' in dash_id:  # Check if the dashboard ID is a LookML dashboard
                    new_dashboard = self.sync_lookml_to_udd(dash_id, dashboard_title)
                else:
                    new_dashboard = self.copy_non_lookml_dashboard(dash_id, dashboard_title)
                new_dashboard_id = new_dashboard.id

                # Update filters in the copied dashboard
                for filter in new_dashboard.dashboard_filters:
                    if filter.name in FILTER_UPDATES:
                        updated_filter = models40.WriteDashboardFilter(
                            allow_multiple_values=filter.allow_multiple_values,
                            dimension=filter.dimension,
                            explore=filter.explore,
                            listens_to_filters=filter.listens_to_filters,
                            required=filter.required,
                            row=filter.row,
                            title=filter.title,
                            default_value=FILTER_UPDATES[filter.name],
                            model=filter.model,
                            name=filter.name,
                            type=filter.type,
                            ui_config=filter.ui_config,
                        )
                        try:
                            self.sdk.update_dashboard_filter(filter.id, updated_filter)
                        except looker_sdk.error.SDKError as e:
                            print(f"Error updating filter {filter.id}: {e.message}")

                # Export specified elements of the new dashboard as PNG images
                dashboard_elements = self.sdk.dashboard_dashboard_elements(dashboard_id=new_dashboard_id)
                for element in dashboard_elements:
                    if element.title in DASHBOARD_DICT[dash_id]:
                        print(f"Exporting element: {element.title}")
                        if element.id:
                            title = element.title or f"element_{element.id}"
                            try:
                                render_task = self.sdk.create_dashboard_element_render_task(element.id,
                                                                                            result_format='png',
                                                                                            width=600, height=800)
                                render_task_id = render_task.id
                                # Wait up to 300 seconds for the render task to complete
                                max_wait_time = 300
                                wait_time = 0
                                while wait_time < max_wait_time:
                                    render_task = self.sdk.render_task(render_task_id)
                                    if render_task.status in ['success', 'failure']:
                                        break
                                    time.sleep(1)  # Wait for 1 second before checking again
                                    wait_time += 1

                                if render_task.status == 'success':
                                    result = self.sdk.render_task_results(render_task_id)
                                    if result:
                                        image_file = f"images/{title}.png"
                                        with open(image_file, "wb") as fh:
                                            fh.write(result)
                                            print(f"Saved {image_file}")
                                    else:
                                        print(f"No data returned for {title}")
                                else:
                                    print(f"Render task for {title} did not complete successfully")
                            except looker_sdk.error.SDKError as e:
                                print(f"Error exporting element {element.id}: {e.message}")

                # Clean up: delete the temporary dashboard
                try:
                    self.sdk.delete_dashboard(new_dashboard_id)
                    print(f"Deleted temporary dashboard with ID: {new_dashboard_id}")
                except looker_sdk.error.SDKError as e:
                    print(f"Error deleting dashboard {new_dashboard_id}: {e.message}")

            except looker_sdk.error.SDKError as e:
                print(f"Error fetching or syncing dashboard {dash_id}: {e}")


# Create an instance of the LookerDashboardManager
manager = LookerDashboardManager(sdk)

# Sync all dashboards
manager.sync_all_dashboards()