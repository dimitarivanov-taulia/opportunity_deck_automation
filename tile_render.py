import time
import looker_sdk
from looker_sdk import models40
import base64

# Initialize Looker SDK
sdk = looker_sdk.init40("looker.ini")
# sdk.delete_dashboard('1782')
# Get all dashboards
# dashboards = sdk.all_dashboards()
# dashboard_info = [(db.id, db.title) for db in dashboards]
# for id, dashboard_name in dashboard_info:
#     print(f"{id} - {dashboard_name}")

# Specify the dashboard ID to copy
dashboard_id = '1767'
dashboard = sdk.dashboard(dashboard_id)

new_dashboard = sdk.copy_dashboard(dashboard_id, '6692')
new_dashboard_id = new_dashboard.id

# Create a copy of the dashboard without filters
# dashboard_copy = models40.WriteDashboard(
#     title=f"Temp Dashboard for {dashboard.title}",
#     description="Temporary dashboard with filters applied",
#     folder_id='6692'  # Use folder_id instead of space_id
# )
# new_dashboard = sdk.create_dashboard(dashboard_copy)
# # new_dashboard_id = new_dashboard.id
#
# # Add filters to the copied dashboard
# for filter in dashboard.dashboard_filters:
#     new_filter = models40.CreateDashboardFilter(
#         name=filter.name,
#         title=filter.title,
#         type=filter.type,
#         default_value=filter.default_value,
#         model=filter.model,
#         explore=filter.explore,
#         dimension=filter.dimension,
#         dashboard_id=new_dashboard_id,
#     )
#     try:
#         sdk.create_dashboard_filter(new_filter)
#     except looker_sdk.error.SDKError as e:
#         print(f"Error creating filter {filter.id}: {e.message}")
#
# # Copy elements from the original dashboard to the new dashboard
# for element in dashboard.dashboard_elements:
#     new_element = models40.WriteDashboardElement(
#         body_text=element.body_text,
#         dashboard_id=new_dashboard_id,
#         look=element.look,
#         look_id=element.look_id,
#         merge_result_id=element.merge_result_id,
#         note_display=element.note_display,
#         note_state=element.note_state,
#         note_text=element.note_text,
#         query=element.query,
#         query_id=element.query_id,
#         refresh_interval=element.refresh_interval,
#         subtitle_text=element.subtitle_text,
#         title=element.title,
#         title_hidden=element.title_hidden,
#         type=element.type,
#     )
#     try:
#         sdk.create_dashboard_element(new_element)
#     except looker_sdk.error.SDKError as e:
#         print(f"Error creating element {element.id}: {e.message}")

# Update specific filters with default values
filter_updates = {
    "Buyer Company Name": 'AcmeBirdSeed',
    "Scenario Description": None,
    "Spend File": 'AcmeBirdSeed_spend_022024',
}

dashboard_render = {
    "Buyer - Payables Benchmark: Industry Benchmarking": ["Peer DPOs",]
}

for filter in new_dashboard.dashboard_filters:
    if filter.name in filter_updates:
        updated_filter = models40.WriteDashboardFilter(
            allow_multiple_values=filter.allow_multiple_values,
            dimension=filter.dimension,
            explore=filter.explore,
            listens_to_filters=filter.listens_to_filters,
            required=filter.required,
            row=filter.row,
            title=filter.title,
            default_value=filter_updates[filter.name],
            model=filter.model,
            name=filter.name,
            type=filter.type,
            ui_config=filter.ui_config,
        )
        try:
            sdk.update_dashboard_filter(filter.id, updated_filter)
        except looker_sdk.error.SDKError as e:
            print(f"Error updating filter {filter.id}: {e.message}")

# Export elements of the new dashboard as PNG images
dashboard_elements = sdk.dashboard_dashboard_elements(dashboard_id=new_dashboard_id)
for element in dashboard_elements:
    print(element.title)
    if element.id:
        title = element.title or f"element_{element.id}"
        try:
            render_task = sdk.create_dashboard_element_render_task(element.id, result_format='png', width=600, height=800)
            render_task_id = render_task.id
            # Wait up to 300 seconds for the render task to complete
            max_wait_time = 350
            wait_time = 0
            while wait_time < max_wait_time:
                render_task = sdk.render_task(render_task_id)
                if render_task.status in ['success', 'failure']:
                    break
                time.sleep(1)  # Wait for 1 second before checking again
                wait_time += 1

            if render_task.status == 'success':
                result = sdk.render_task_results(
                    render_task_id,
                )
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
    sdk.delete_dashboard(new_dashboard_id)
    print(f"Deleted temporary dashboard with ID: {new_dashboard_id}")
except looker_sdk.error.SDKError as e:
    print(f"Error deleting dashboard {new_dashboard_id}: {e.message}")
