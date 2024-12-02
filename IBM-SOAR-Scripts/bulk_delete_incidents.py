import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import os
import logging

urllib3.disable_warnings()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from file
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
logging.info(f"Config file path: {config_path}")

try:
    with open(config_path) as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    logging.error("Configuration file not found.")
    exit(1)
except json.JSONDecodeError:
    logging.error("Error decoding JSON configuration file.")
    exit(1)

KEY_ID = config['key_id']
KEY_SECRET = config['key_secret']
SERVER = config['server']
ORG_ID = config['org_id']

HEADERS = {"Content-Type": "application/json"}
AUTH = HTTPBasicAuth(KEY_ID, KEY_SECRET)

def send_request(method, resource, data=None):
    url = f"https://{SERVER}/{resource}"
    try:
        if method == 'POST':
            response = requests.post(url, headers=HEADERS, auth=AUTH, verify=False, data=data)
        elif method == 'PUT':
            response = requests.put(url, headers=HEADERS, auth=AUTH, verify=False, data=data)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def get_incidents_ids_by_filter(creator_id, plan_status, number_of_incidents=0):
    resource = f"rest/orgs/{ORG_ID}/incidents/query_paged"

    # Filter to get all incidents by creator_id and plan_status
    body = json.dumps({
        "filters": [
            {
                "conditions": [
                    {"method": "equals", "field_name": "creator_id", "value": creator_id},
                    {"method": "equals", "field_name": "plan_status", "value": plan_status}
                ]
            }
        ],
        "sorts": [{"field_name": "plan_status", "type": "desc"}],
        "start": 0,
        "length": number_of_incidents,
        "recordsTotal": 0
    })
    response = send_request('POST', resource, body)
    if response:
        return response.json()
    return None

def create_test_incident():
    resource = f"rest/orgs/{ORG_ID}/incidents"
    body = json.dumps({
        "name": "Incident from Python script",
        "description": "Very bad incident",
        "discovered_date": 0
    })
    response = send_request('POST', resource, body)
    return response

def bulk_create_test_incidents(number_of_incidents):
    for i in range(number_of_incidents):
        create_test_incident()
        logging.info(f"Created incident {i+1}")

def delete_incident(id):
    resource = f"rest/orgs/{ORG_ID}/incidents/delete"
    body = json.dumps([id])
    response = send_request('PUT', resource, body)
    if response and response.status_code == 200:
        logging.info(f"Successfully deleted incident {id}")
    else:
        logging.error(f"Failed to delete incident {id}")
    return response

def bulk_delete_incidents(ids, number_of_incidents):
    for i in range(number_of_incidents):
        response = delete_incident(ids[i])
        if response and response.status_code == 200:
            logging.info(f"Deleted incident {i+1}")
        else:
            logging.error(f"Failed to delete incident {i+1}")

def main():
    # creator_id is the id of the user who created the incident
    # To get the id of the user who created the incident, you can use the interactive REST API
    # Go to TypesREST endpoint > GET /orgs/{org_id}/types/{type}/fields/{field}
    # Set the type = incident and field = creator_id
    # Or replace creator_id with your custom field
    creator_id = 28

    # plan_status is the status of the incident
    # A - Active
    # C - Closed
    plan_status = "A"

    # Number of incidents to get. Set to 0 to get all incidents
    number_of_incidents_to_get = 0

    # Number of incidents to delete
    number_of_incidents_to_delete = 5

    # Get incidents by filter and delete the specified number of incidents
    incidents = get_incidents_ids_by_filter(creator_id, plan_status, number_of_incidents_to_get)
    if incidents:
        ids = [item['id'] for item in incidents['data']]
        logging.info(f"Incident IDs: {ids}")
        bulk_delete_incidents(ids, number_of_incidents_to_delete)
    else:
        logging.error("Failed to retrieve incidents.")

    
    #Create test incidents
    bulk_create_test_incidents(5)

    


if __name__ == "__main__":
    main()
