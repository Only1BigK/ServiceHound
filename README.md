
# ServiceHound - BloodHound to ServiceNow 

### ABOUT
This integration connects BloodHound to ServiceNow via their API. It automatically creates tickets in ServiceNow, including a title, a detailed description with information about the principals involved, the source principal, the target principal, remediation steps and BHE AttackPath Description. Additionally, it updates the severity ratings of existing tickets if changes occur within BloodHound aswell as the description.

## Installation/Requirements:
#### Necessary Components
1. Python 3.x (developed with Python 3.12)
2. BloodHound API [ https://support.bloodhoundenterprise.io/hc/en-us/articles/11311053342619-Working-with-the-BloodHound-API ]

#### Packages:
1. dotenv
2. requests 

## Usage
Instructions on how to use the project:
1. Replace the following with your own data.
```
url = "[YOUR SERVICE NOW API ENDPOINT]"
username = os.getenv("[SERVICE NOW USERNAME]")
password = os.getenv("[SERVICE NOW PASSWD]")
```
```
credentials = Credentials(os.getenv('[YOUR BLOODHOUND_TOKEN_ID]'), os.getenv('[YOUR BLOODHOUND_TOKEN_KEY]'))
client = BHEClient('https', '[YOUR BLOODHOUND ENTERPRISE URL]', 443, credentials)
```

Update the impact_score and urgency_score values to your liking.
```
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
```

```
incident_data = {
    ....
    "assignment_group": "YOUR ASSIGNMENT GROUP"
}
```

2. If you would like to enable or disable updates for urgency_score and impact_score and descriptions, comment or uncomment the following lines of code:

To disable/enable the automatic updates of impact and urgency within your ServiceNow environment comment or uncomment the following:
```
## Update Severity If Needed
if response.json()['result'][0].get('impact') != str(impact_score) or response.json()['result'][0].get('urgency') != str(urgency_score):
    update_data={
        "impact": impact_score,
        "urgency": urgency_score
    }
    print(f"[UPDATED]: {response.json()['result'][0]['number']}")

    requests.patch(f"{url}/{response.json()['result'][0].get('sys_id')}", auth=(username,password), json=update_data)
```

To disable/enable the automatic updates for the description within your ServiceNow environment comment or uncomment the following:
```
if response.json()['result'][0].get('description') != description:
    update_data={
        "description": description
    }
    print(f"[UPDATED] Description for: {response.json()['result'][0]['number']}")
    requests.patch(f"{url}/{response.json()['result'][0].get('sys_id')}", auth=(username,password), json=update_data)
```

3. By default the limit to pull is set to 10, this will only pull the first 10 principals avaliable within the BHE platform, to increase this and to push all 
principals to the ServiceNow ticket uncomment this code 
```
## NOTE: Some findings can have a count of over 100, so enable if you are sure you want everything within the Ticket.
if details['limit'] != details['count'] and details['count'] > 10:
    print(details['count'])
    details = client.get_finding_details(finding, limit=details['count'])
```


## To-Do
- [x] Post BloodHound Data to ServiceNow.
- [x] Update SNOW Incidents priority based on the new impact and urgency.
- [x] Update SNOW Incidents with latest BHE description/data e.g (BHE Description, principals involved, source principal, target principal, and remediation steps).
- [x] Increase the amount of principals pulled and sent to ServiceNow, for ticket creation.
- [ ] Implement User friendly customisation options.