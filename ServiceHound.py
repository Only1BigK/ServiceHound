###########################
#
# Created By: Elie Ajaka
# https://github.com/Eli4m
# 
# Licence: MIT License
# 
###########################

from BloodHoundAPICalls import *
import os 
from dotenv import load_dotenv
import requests
import sys

load_dotenv()
currentDir = os.getcwd()

## ServiceNow Setup.
url = "[YOUR SERVICE NOW API ENDPOINT]"
username = os.getenv("[SERVICE NOW USERNAME]")
password = os.getenv("[SERVICE NOW PASSWD]")

## Verify Valid URL. 
try:
    requests.get(url=url)
except:
    print(f"Can not connect to {url}. Aborting!")
    sys.exit(1)

## Blood Hound Setup.
credentials = Credentials(os.getenv('[YOUR BLOODHOUND_TOKEN_ID]'), os.getenv('[YOUR BLOODHOUND_TOKEN_KEY]'))
client = BHEClient('https', '[YOUR BLOODHOUND ENTERPRISE URL]', 443, credentials)

## Initial Setup.
domains = client.get_domains()

## Gets findings for all domains.
domain_findings = [] 
for domain in domains:
    try:
        domain_findings += client.get_findings(domain)
    except Exception as e:
        print(f"Error fetching finding for domain {domain.id}: {e}")

## Iterate through findings and pull relevant data. 
for finding in domain_findings:
    title = f"{finding.domain_name} - {client.get_finding_title_Updated(finding.id)}"
    
    ## You can increase the finding count here if necessary, default is 10. E.g client.get_finding_details(finding, 50)
    details = client.get_finding_details(finding)

    ## Updated BHE python integration script, was required as the doc has been relocated from /ui/findings/ to /api/v2/assets/findings/
    description = f"Description: \n{client.get_finding_documentation_Updated(finding.id, 'short_description')}\n\n"
    description += f"Remediation: \n{client.get_finding_documentation_Updated(finding.id, 'short_remediation')}\n"

    ## Update the count to max count if you want all the finding data stored in the service now ticket
    ## NOTE: Some findings can have a count of over 100 so enable if you are sure you want everything within the Ticket.
    # if details['limit'] != details['count'] and details['count'] > 10:
    #     print(details['count'])
    #     details = client.get_finding_details(finding, limit=details['count'])

    for i in range(0, len(details['data'])):
        description += f"\nFromPrincipal ID: {details['data'][i].get('FromPrincipal')}\n"
        description += f"FromPrincipalName: {details['data'][i].get('FromPrincipalProps').get('name')}\n"
        description += f"ToPrincipal ID: {details['data'][i].get('ToPrincipal')}\n"
        description += f"ToPrincipalName: {details['data'][i].get('ToPrincipalProps').get('name')}\n"
        # description += f"Principal: {details['data'][i].get('Principal')}\n"

    priority_classification = get_severity(client.get_finding_timeline_no_range(finding)['data'][0].get('CompositeRisk'))
    impact_score = 0
    urgency_score = 0

    ## Customise values to your liking.
    match priority_classification:
        case "Low":
            impact_score = 0
            urgency_score = 0
        case "Medium":
            impact_score = 0
            urgency_score = 0
        case "High":
            impact_score = 0
            urgency_score = 0
        case "Critical":
            impact_score = 0
            urgency_score = 0

    incident_data = {
        "short_description": title,
        "description": description,
        "impact": impact_score,
        "urgency": urgency_score,
        "assignment_group": "[YOUR ASSIGNMENT GROUP]"
    }
    
    ## Ensure html pages are not sent to service now 
    ## Issue arrises when bloodhound api integration is broken i.e when pulling specific .md data that no longer exists or has been relocated 
    manualReview = False
    if "<html>" in description or "<!doctype html>" in description or "<html>" in title or "<!doctype html>" in title:
        with open(f"{currentDir}\\Error.log", "a") as outfile: 
            outfile.write(f"Error While Pulling Data, Debug Script, [TIP] - Review BloodHound and SNOW API Connections \
                          to ensure nothing is broken.\n")
            
            print("Error While Pulling Data, Debug Script, [TIP] - Review BloodHound and SNOW API Connections to ensure nothing is broken.")
        manualReview = True

    ## Handle requests to ServiceNow (SNOW)
    if not manualReview:
        response = requests.get(url, auth=(username,password), params={'short_description': title})

        if response.status_code == 200 and response.json()['result']:
            print(f"Incident already exists! Incident number: {response.json()['result'][0]['number']}")
            
            # ## NOTE: Uncomment to Update Severity If Needed.
            # if response.json()['result'][0].get('impact') != str(impact_score) or response.json()['result'][0].get('urgency') != str(urgency_score):
            #     update_data={
            #         "impact": impact_score,
            #         "urgency": urgency_score
            #     }
            #     print(f"[UPDATED] Severity for: {response.json()['result'][0]['number']}")
            #     requests.patch(f"{url}/{response.json()['result'][0].get('sys_id')}", auth=(username,password), json=update_data)

            # ## NOTE: Uncomment to Update Description If Needed.
            # if response.json()['result'][0].get('description') != description:
            #     update_data={
            #         "description": description
            #     }
            #     print(f"[UPDATED] Description for: {response.json()['result'][0]['number']}")
            #     requests.patch(f"{url}/{response.json()['result'][0].get('sys_id')}", auth=(username,password), json=update_data)
        else:
            response = requests.post(url, auth=(username,password), json=incident_data)
            if response.status_code == 201:
                print(f"Incident Created Successfully! Incident number: {response.json().get('result').get('number')}")
            else:
                print(f"Error creating incident. Status code: {response.status_code}")
    else:
        print ("This Alert requires manual review as HTML tags were found in its title or description contents.")