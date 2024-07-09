import looker_sdk  # access looker objects
from looker_sdk import models40
import base64  # encode looker image into .png file
import os  # only necessary if assigning Looker SDK connection information to environment variables

filter_dict = {}

sdk = looker_sdk.init40("looker.ini")
dashboards = sdk.all_dashboards()
dashboard_info = [(db.id, db.title) for db in dashboards]
for id, dashboard_name in dashboard_info:
    print(f"{id} - {dashboard_name}")
# dashboard_id = str(input("Select Dashboard:"))
dashboard_id = '1767'
dashboard = sdk.dashboard(dashboard_id)

# Create a copy of the dashboard without filters
dashboard_copy = models40.WriteDashboard(
    title=f"Temp Dashboard for {dashboard.title}",
    description="Temporary dashboard with filters applied",
    folder_id='6692'  # Use folder_id instead of space_id
)
new_dashboard = sdk.create_dashboard(dashboard_copy)
new_dashboard_id = new_dashboard.id
# new_dashboard_id = '1768'
# new_dashboard = sdk.dashboard(new_dashboard_id)

# print(f"Created temporary dashboard with ID: {new_dashboard_id}")

# Add filters to the copied dashboard
for filter in dashboard.dashboard_filters:
    new_filter = models40.CreateDashboardFilter(
        name=filter.name,
        title=filter.title,
        type=filter.type,
        default_value=filter_dict.get(filter.name, filter.default_value),
        model=filter.model,
        explore=filter.explore,
        dimension=filter.dimension,
        dashboard_id=new_dashboard_id,
    )
    sdk.create_dashboard_filter(new_filter)


# Copy elements from the original dashboard to the new dashboard
for element in dashboard.dashboard_elements:
    new_element = models40.WriteDashboardElement(
        body_text=element.body_text,
        dashboard_id=new_dashboard_id,
        look=element.look,
        look_id=element.look_id,
        merge_result_id=element.merge_result_id,
        note_display=element.note_display,
        note_state=element.note_state,
        note_text=element.note_text,
        query=element.query,
        query_id=element.query_id,
        refresh_interval=element.refresh_interval,
        subtitle_text=element.subtitle_text,
        title=element.title,
        title_hidden=element.title_hidden,
        type=element.type,
    )
    try:
        sdk.create_dashboard_element(new_element)
    except looker_sdk.error.SDKError as e:
        print(f"Error creating element {element.id}: {e.message}")

for filter in dashboard.dashboard_filters:
    print(f"name: {filter.name} - filterid: {filter.id} -model:{filter.model} type {filter.type}")
    filter_name = filter.name
    filter_id = filter.id
    filter_model = filter.model
    filter_type = filter.type

    if filter_name == "Buyer Company Name":
        default_value = "AcmeBirdSeed"
        updated_filter = models40.WriteDashboardFilter(
            allow_multiple_values=filter.allow_multiple_values,
            dimension=filter.dimension,
            explore=filter.explore,
            listens_to_filters=filter.listens_to_filters,
            required=filter.required,
            row=filter.row,
            title=filter.title,
            default_value=default_value,
            model=filter.model,
            name=filter.name,
            type=filter.type,
            ui_config=filter.ui_config,
        )
        sdk.update_dashboard_filter(filter_id, updated_filter)

    if filter_name == "Scenario Description":
        default_value = "No Term Extension"
        updated_filter = models40.WriteDashboardFilter(
            allow_multiple_values=filter.allow_multiple_values,
            dimension=filter.dimension,
            explore=filter.explore,
            listens_to_filters=filter.listens_to_filters,
            required=filter.required,
            row=filter.row,
            title=filter.title,
            default_value=default_value,
            model=filter.model,
            name=filter.name,
            type=filter.type,
            ui_config=filter.ui_config
        )
        response = sdk.update_dashboard_filter(filter_id, updated_filter)
        print(response)


    if filter_name == "Spend File":
        default_value = "AcmeBirdSeed_spend_012024"
        updated_filter = models40.WriteDashboardFilter(
            allow_multiple_values=filter.allow_multiple_values,
            dimension=filter.dimension,
            explore=filter.explore,
            listens_to_filters=filter.listens_to_filters,
            required=filter.required,
            row=filter.row,
            title=filter.title,
            default_value=default_value,
            model=filter.model,
            name=filter.name,
            type=filter.type,
            ui_config=filter.ui_config
        )
        sdk.update_dashboard_filter(filter_id, updated_filter)

dashboard_elements = sdk.dashboard_dashboard_elements(dashboard_id=new_dashboard_id)
for element in dashboard_elements:
    if element.query_id:
        title = element.title or f"element_{element.id}"
        query_image = sdk.run_query(element.query_id, result_format='png')
        image_file = f"{title}.png"
        with open(image_file, "wb") as fh:
            fh.write(query_image)
        print(f"Saved {image_file}")

# Clean up: delete the temporary dashboard
try:
    sdk.delete_dashboard(new_dashboard_id)
    print(f"Deleted temporary dashboard with ID: {new_dashboard_id}")
except looker_sdk.error.SDKError as e:
    print(f"Error deleting dashboard {new_dashboard_id}: {e.message}")

# # run each element in the dashboard and apply the dashboard filters. Then, save the file in .png format.
# for element in dashboard.dashboard_elements:
#     print(element.query_id)
#     # create a copy of the tile query to apply filters to
# element.query = filter_dict
# altered_query = element.query
# title = element.title
# # if the query has existing filters, append the dashboard filters
# if 'filters' in altered_query:
#     altered_query.filters.update(filter_dict)
# if 'filters' not in altered_query:
#     altered_query['filters'] = filter_dict
#     # remove the client id and id from the query to create a new query
#     altered_query.client_id = None
#     altered_query.id = None
#     # run the query with applied filters inline (doesn't create a new query object) and save as .png file
#     query_image = sdk.run_inline_query(body=altered_query, result_format='png')
#     image_string = base64.b64encode(query_image)
#     image_file = '.'.join([title, 'png'])
#     with open(image_file, "wb") as fh:
#         fh.write(base64.decodebytes(image_string))
