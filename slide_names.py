
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
