
# Slide names
# Cover Page
# Situation Summary
# Text only (ignore)
# Current And Target Terms
# Current Terms
# Current Terms (Business Unit specific) - this is for Airbus, something specific
# Liquidity Demand & Discount Potential across APR
# Peer CCC Benchmark
# Peer DSO Benchmark

# Not Standard - ??

# Program Segmentation
    # this should be done manually by the sales person as I see from the presentation, there is no chart
    # here is checked the addressable spend, supplier with more or less that 15 days terms
    # the segmentation is based on spend and term length

# Top 10 suppliers (non-excluded)
    # this should be the same as Top 10 suppliers with WC opportunity
    # or here we should check the spend, not the WC opportunity

# Top 10 suppliers with WC opportunity
# https://looker.na1prd-bi.taulia.com/dashboards/payables_planner::buyer__payables_planner_supplier_list?Reporting+Currency=USD&Other+Currency=AED&Buyer+Company+Name=&Spend+File=&Buyer+Business+Unit=&Buyer+Business+Unit+Country=&Payment+Currency=&Supplier+Country=&Currency+Trios=&Supplier+Industry=&Supplier+Industry+Sector=&Supplier+Terms=%3E%3D0&Supplier+Addressable=Addressable%2CExcluded&Scenario+Description=&Supplier+Segment+Name=&Business+Case+Class=Recent&Funding+Options=Flexible+Funding
# payables_planner::buyer__payables_planner_supplier_list
# Buyer - Payables Planner Supplier List
# this a table, no name
# after the table is sorted for the right business case, the suppliers have to be ordered by WC potential DESC
filter_updates = {
    "Buyer Company Name": 'American Water',
    "Spend File": 'American_Water_custom_022024',
    "Scenario Description": '',
    "Supplier Terms": '', # higher than 15, less, etc..
    "Buyer APR Floor": '',
    "Supplier Addressable": '' #only the addressable
    # and maybe others
}
# this is also in Connor's folder
# https://looker.na1prd-bi.taulia.com/dashboards/165?Scenario+Description=&Term+Extension+Adoption=1&Buyer+Funding+Percent=100&Buyer+APR+Floor=6&Reporting+Currency=USD&Other+Currency=AED&Buyer+Company+Name=American+Water&Spend+File=%22American_Water_custom_022024%22&Buyer+Business+Unit=&Buyer+Business+Unit+Country=&Payment+Currency=&Supplier+Country=&Currency+Trios=&Supplier+Industry=&Supplier+Industry+Sector=&Supplier+Spend=%3E%3D0&Supplier+Terms=%3E%3D0&Supplier+Addressable=Addressable&Supplier+Segment+Name=&Visualize+Unknown+Industry+Sector=Unknown&Business+Case+Class=Recent&Funding+Options=Flexible+Funding
# Connor Eddy - Working Capital Focus
# table name: Top 25 WC Potential Suppliers
# same filters

# WC Opportunity by adoption %
# https://looker.na1prd-bi.taulia.com/dashboards/165?Scenario+Description=&Term+Extension+Adoption=1&Buyer+Funding+Percent=100&Buyer+APR+Floor=6&Reporting+Currency=USD&Other+Currency=AED&Buyer+Company+Name=&Spend+File=&Buyer+Business+Unit=&Buyer+Business+Unit+Country=&Payment+Currency=&Supplier+Country=&Currency+Trios=&Supplier+Industry=&Supplier+Industry+Sector=&Supplier+Spend=%3E%3D0&Supplier+Terms=%3E%3D0&Supplier+Addressable=Addressable&Supplier+Segment+Name=&Visualize+Unknown+Industry+Sector=Unknown&Business+Case+Class=Recent&Funding+Options=Flexible+Funding
# in Connor's folder - Working Capital Focus
# chart name: there is no name of this chart
filter_updates = {
    "Buyer Company Name": 'American Water',
    "Spend File": 'American_Water_custom_022024',
    "Scenario Description": '',
    "Supplier Terms": '', # higher than 15, less, etc..
    "Buyer APR Floor": ''
    # and maybe others
}

# Top 10 Industry Term/DSO Comparison
# Buyer - Payables Benchmark
# https://looker.na1prd-bi.taulia.com/dashboards/payables_benchmark::buyer__payables_benchmark?Reporting+Currency=USD&Other+Currencies=AED&Buyer+Company+Name=American+Water&Spend+File=%22American_Water_custom_022024%22&Buyer+Business+Unit=&Buyer+Business+Unit+Country=&Payment+Currency=&Supplier+Country=&Supplier+Industry=&Supplier+Spend=%3E%3D0&Supplier+Terms=%3E%3D0&Supplier+Addressable=Addressable%2CExcluded&Supplier+Segment+Name=&Median%2F3rd+Quartile=3rdquart&Show+Supplier+Terms+by=Industry+Sector&Visualize+Unknown+Industry+Sector=Unknown&Peer+Country=&Peer+Company=&Peer+Industry=&Peer+Revenue=&Peer+Region=&Business+Case+Class=Recent
# payables_benchmark::buyer__payables_benchmark
# chart name: Supplier Payment Terms Comparison
filter_updates = {
    "Buyer Company Name": 'American Water',
    "Spend File": 'American_Water_custom_022024'
}
        # the more correct one is in Connor's folder - has the blue line like in the presentation
# https://looker.na1prd-bi.taulia.com/dashboards/165?Scenario+Description=&Term+Extension+Adoption=1&Buyer+Funding+Percent=100&Buyer+APR+Floor=6&Reporting+Currency=USD&Other+Currency=AED&Buyer+Company+Name=&Spend+File=&Buyer+Business+Unit=&Buyer+Business+Unit+Country=&Payment+Currency=&Supplier+Country=&Currency+Trios=&Supplier+Industry=&Supplier+Industry+Sector=&Supplier+Spend=%3E%3D0&Supplier+Terms=%3E%3D0&Supplier+Addressable=Addressable&Supplier+Segment+Name=&Visualize+Unknown+Industry+Sector=Unknown&Business+Case+Class=Recent&Funding+Options=Flexible+Funding
# Connor Eddy - Working Capital Focus
# chart name: Industry Term Comparison
filter_updates = {
    "Buyer Company Name": 'American Water',
    "Spend File": 'American_Water_custom_022024',
    "Scenario Description": '',
    "Supplier Terms": '', # higher than 15, less, etc..
    "Buyer APR Floor": ''
    # and maybe others
}

# Peer DPO Benchmark
# Buyer - Payables Benchmark
# https://looker.na1prd-bi.taulia.com/dashboards/payables_benchmark::buyer__payables_benchmark?Reporting+Currency=USD&Other+Currencies=AED&Buyer+Company+Name=&Spend+File=&Buyer+Business+Unit=&Buyer+Business+Unit+Country=&Payment+Currency=&Supplier+Country=&Supplier+Industry=&Supplier+Spend=%3E%3D0&Supplier+Terms=%3E%3D0&Supplier+Addressable=Addressable%2CExcluded&Supplier+Segment+Name=&Median%2F3rd+Quartile=3rdquart&Show+Supplier+Terms+by=Industry+Sector&Visualize+Unknown+Industry+Sector=Unknown&Peer+Country=&Peer+Company=&Peer+Industry=&Peer+Revenue=&Peer+Region=&Business+Case+Class=Recent
# payables_benchmark::buyer__payables_benchmark
# chart name: Peer DPO
filter_updates = {
    "Buyer Company Name": 'American Water'
}

# V Card Analysis
# Buyer - Payables Benchmark
# https://looker.na1prd-bi.taulia.com/dashboards/payables_benchmark::buyer__payables_benchmark?Reporting+Currency=USD&Other+Currencies=AED&Buyer+Company+Name=&Spend+File=&Buyer+Business+Unit=&Buyer+Business+Unit+Country=&Payment+Currency=&Supplier+Country=&Supplier+Industry=&Supplier+Spend=%3E%3D0&Supplier+Terms=%3E%3D0&Supplier+Addressable=Addressable%2CExcluded&Supplier+Segment+Name=&Median%2F3rd+Quartile=3rdquart&Show+Supplier+Terms+by=Industry+Sector&Visualize+Unknown+Industry+Sector=Unknown&Peer+Country=&Peer+Company=&Peer+Industry=&Peer+Revenue=&Peer+Region=&Business+Case+Class=Recent
# payables_benchmark::buyer__payables_benchmark
# chart name Card Adoption
filter_updates = {
    "Buyer Company Name": 'American Water'
    # should we choose file description here??
}










# filter_updates = {
#     "Buyer Company Name": 'AcmeBirdSeed',
#     "Scenario Description": None,
#     "Spend File": 'AcmeBirdSeed_spend_022024',
# }
#
# {
# Funding Option: None, #comment based on what the Opportunity Type (DD SCF or Flexible),
# Buyer APR Floor: None, #based on What is the customer's floor rate? (%)
# Supplier Terms: 15, #based on analyst input
# }


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 14:00:28 2023

@author: daniel.lozanov
"""

import requests
import json

client_id = "xxxx"
client_secret = "xxxx"


class class_run_looks_with_filters:
    def __init__(self,client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    # Get access token
    def authenticate(self):
        self.access_token = json.loads(requests.post("https://looker-api.integration-bi.taulia.com/api/4.0/login",
                                               data = {"client_id": self.client_id,
                                                       "client_secret": self.client_secret},
                                               timeout = 60).content)['access_token']
        print("Access token generated!")

    #Get all Looks and find the ones we want and fetch the metadata of the look, so we can overwrite filters later on
    def resolve_look_metadata_by_name(self, lookup_folder, lookup_looks_in_folder):
        list_looks = json.loads(requests.get("https://looker-api.integration-bi.taulia.com/api/4.0/looks",
                                               headers = {"Authorization": "token "+str(self.access_token)},
                                               timeout = 60).content)

        self.look_ids = {}
        for i in list_looks:
            if i['folder']['name'] == lookup_folder and i['title'] in lookup_looks_in_folder:
                print("Found Look '{title}' inside folder {folder} which has Look_id = {look_id}".format(title = i['title'], folder = lookup_folder, look_id = i['id']))
                self.look_ids[i['title']] = json.loads(requests.get("https://looker-api.integration-bi.taulia.com/api/4.0/looks/"+str(i['id']),
                                               headers = {"Authorization": "token "+str(self.access_token)},
                                               timeout = 60).content)['query']



    def run_inline_query_with_extra_filters(self, look_name, filters = {}):
        #pass look_name(str), and dictionary filters(dict)

        #mandatory properties for each query. This will bring all needed info how the tile works and which resources does it access
        #note that the tile can have "filters" attribute here, which are default tile flters, brought by the tile itself.
        #any filters we would like to apply should overwrite and apply on-top of what we currently have.
        query_requirements = ['model', 'view', 'fields', 'pivots',
                              'fill_fields', 'filters', 'sorts', 'limit',
                              'column_limit', 'total', 'row_total', 'subtotals',
                              'dynamic_fields', 'query_timezone']

        query_payload = {}
        for i in query_requirements:
            query_payload[i] = self.look_ids[look_name][i]

        #now ehchance with the filters we would like to apply:
        for i in filters.keys():
            if ( query_payload['filters'] is None ):
                query_payload['filters'] = {}

            query_payload['filters'][i] = filters[i]

        #run the query now...
        #example {
        #   "model": "business_case_set", "view": "ep_prospects_business_case",
        #   "fields": ["ep_prospects_business_case_details.total_annual_spend"],
        #   "pivots": null, "fill_fields": null,
        #   "filters": {"ep_prospects_business_case_details.supplier_country_code": "DE"},
        #   "sorts": [], "limit": "500", "column_limit": null, "total": null,
        #   "row_total": null, "subtotals": null, "dynamic_fields": null, "query_timezone": null
        #   }
        print("")
        print("-RUNNING-----")
        print(json.dumps(query_payload))
        print("-------------")
        run_query_look_data = json.loads(requests.post("https://looker-api.integration-bi.taulia.com/api/4.0/queries/run/json",
                                               headers = {"Authorization": "token "+str(self.access_token)},
                                               data = json.dumps(query_payload),
                                               timeout = 60).content)

        print("result >> "+json.dumps(run_query_look_data))
        return run_query_look_data

    def get_dashboard_by_title_and_folder(self, lookup_dashboard_name, lookup_folder):
        #maybe we do not need to run 2 api calls here, let's stick with 1.
        #two if we would also pass folder id(needs API request to retrieve folder id by folder name ..) in the payload below, rather than, let's just search by name,
        #retrieve all matching dashboards and then look through the result to narrow it down to the desired folder?
        dashboard_data = json.loads(requests.get("https://looker-api.integration-bi.taulia.com/api/4.0/dashboards",
                                                  headers = {"Authorization": "token "+str(self.access_token)},
                                                  data = {"title": lookup_dashboard_name},
                                                  timeout = 60).content)

        for i in dashboard_data:
            if i['folder']['name'] == lookup_folder and i['title'] == lookup_dashboard_name:
                print("Found dashboard with id = "+str(i['id']))
                return i
        return None

    def get_dashboard_metadata_filters(self, dashboard_id):
        data = json.loads(requests.get("https://looker-api.integration-bi.taulia.com/api/4.0/dashboards/"+str(dashboard_id)+"/dashboard_filters",
                                                           headers = {"Authorization": "token "+str(self.access_token)},
                                                           timeout = 60).content)
        print("Found "+str(len(data))+" filters for dashboard with id "+str(dashboard_id))
        return data

    def get_all_dashboard_elements(self, dashboard_id):
        data = json.loads(requests.get("https://looker-api.integration-bi.taulia.com/api/4.0/dashboards/"+str(dashboard_id)+"/dashboard_elements",
                                                           headers = {"Authorization": "token "+str(self.access_token)},
                                                           timeout = 60).content)
        return data



if __name__ == "__main__":

    looker_connection = class_run_looks_with_filters(client_id, client_secret)
    looker_connection.authenticate()
    looker_connection.resolve_look_metadata_by_name(lookup_folder = "Daniel Lozanov",
                                                    lookup_looks_in_folder = ['Business Case KPIs', 'Spend Analyzed', 'Spend in Scope', 'Supplier Count'])
    #^^ maybe we no longer need to have multiple looks. Business Case KPIs will manage all data inquiry in one shot...

    #this is which tiles we found:
    print(looker_connection.look_ids.keys())

    #now let's try running 'Spend in Scope' tile with few different filters.
    """
    looker_connection.run_inline_query_with_extra_filters(look_name = "Spend in Scope",
                                                          filters = {})
    #^^ Total around 350Bn

    looker_connection.run_inline_query_with_extra_filters(look_name = "Spend in Scope",
                                                          filters = {'ep_prospects_business_case_details.supplier_country_code': 'US'})
    #^^ expected US ~141.1Bn. Can vary as we run/update integration business case data..

    looker_connection.run_inline_query_with_extra_filters(look_name = "Spend in Scope",
                                                          filters = {'ep_prospects_business_case_details.supplier_country_code': 'DE'})
    #^^ expected DE ~98.0Bn. Can vary as we run/update integration business case data..
    """

    looker_connection.run_inline_query_with_extra_filters(look_name = "Business Case KPIs",
                                                          filters = {})

    looker_connection.run_inline_query_with_extra_filters(look_name = "Business Case KPIs",
                                                          filters = {'ep_prospects_business_case_details.supplier_country_code': 'BG'})



    """
    #now let's see what we can do with the filters?
    opp_assess_dashboard = looker_connection.get_dashboard_by_title_and_folder(lookup_dashboard_name = "Buyer - Scenario Planner: Opportunity Assessment",
                                                                               lookup_folder = "Daniel Lozanov")


    opp_assess_dashboard_filters = looker_connection.get_dashboard_metadata_filters(opp_assess_dashboard['id'])

    all_dashboard_elements = looker_connection.get_all_dashboard_elements(opp_assess_dashboard['id'])
    """
