# -*- coding: utf-8 -*-
from __future__ import print_function
from requests.auth import HTTPBasicAuth
import requests
import json


def main():
    key_id = "YOUR-KEY-ID"
    key_secret = "YOUR-KEY-SECRET"

    server = "YOUR-IBM-SOAR-FQDN"
    resource = "rest/orgs/201/incidents"
    url = "https://{0}/{1}".format(server, resource)
    headers = {"Content-Type": "application/json"}

    name_of_the_incident = "Incident from Python script"
    description_of_the_incident = "Very bad incident"

    auth = HTTPBasicAuth(key_id, key_secret)
    req = requests.post(url, headers=headers, auth=auth, verify=False, data=json.dumps(
        {"name": name_of_the_incident, "description": description_of_the_incident, "discovered_date": 0}))


if __name__ == "__main__":
    main()
