# ServiceHound - BloodHound to ServiceNow

## ABOUT
This integration connects BloodHound to ServiceNow via their API. It automatically creates tickets in ServiceNow, including a title, a detailed description with information about the, principals involved, the source principal, the target principal, remediation steps and BHE AttackPath Description. Additionally, it updates the severity ratings of existing tickets if changes occur within BloodHound.

## Installation/Requirerments
Requierments:
1. Python 3.12
2. BloodHound API [ https://support.bloodhoundenterprise.io/hc/en-us/articles/11311053342619-Working-with-the-BloodHound-API ]


Packages:
1. dotenv
3. requests 

## Usage
Instructions on how to use the project:
1. Replace the following with your own data.
```
.....
url = "[YOUR SERVICE NOW API ENDPOINT]"
username = os.getenv("[SERVICE NOW USERNAME]")
password = os.getenv("[SERVICE NOW PASSWD]")
.....
```
```
.....
credentials = Credentials(os.getenv('[YOUR BLOODHOUND_TOKEN_ID]'), os.getenv('[YOUR BLOODHOUND_TOKEN_KEY]'))
client = BHEClient('https', '[YOUR BLOODHOUND ENTERPRISE URL]', 443, credentials)
.....
```

Update the impact_score and urgency_score based off your risk appetite.
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
    .....
    "assignment_group": "YOUR ASSIGNMENT GROUP"
}
```

2. Disabling updates for uregency_score and impact_score

To disable the automatic updates of impact and urency within your ServiceNow environment remove the following from the codebase:
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

## To-Do
- [x] Post BloodHound Data to ServiceNow.
- [x] Update SNOW Incidents priority based on the new impact and urgency.
- [ ] Update SNOW Incidents with latest BHE description/data i.e (BHE Description, principals involved, source principal, target principal, and remediation steps).