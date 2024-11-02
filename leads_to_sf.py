import requests
import json
import pandas as pd
from simple_salesforce import Salesforce
from logging import getLogger, StreamHandler, DEBUG

# set up logger
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

# your user name and password to your Salesforce Org
uname = 'xyz@yoursalesforceOrg.com'
passwd = 'YourPassword'

consumer_key = 'Your Consumer Key from your Salesforce Org'
consumer_secret = 'Your Consumer Secret from your Salesforce Org'

# stanard URLs of Salesforce
request_token_url = 'https://login.salesforce.com/services/oauth2/token'
access_token_url = 'https://login.salesforce.com/services/oauth2/token'
authorize_url = 'https://login.salesforce.com/services/oauth2/authorize'
redirect_uri = 'https://localhost/callback'

data = {
    'grant_type': 'password',
    'client_id': consumer_key,
    'client_secret': consumer_secret,
    'username': uname,
    'password': passwd
}

headers = {
    'content-type': 'application/x-www-form-urlencoded'
}

req = requests.post(access_token_url, data=data, headers=headers)
response = req.json()
logger.debug(response)

sf = Salesforce(instance_url=response['instance_url'], session_id=response['access_token'])

records = sf.query("SELECT Id, Name, Email from Contact")
records = records['records']
for record in records:
    pretty_json = json.dumps(records, indent=2)

# Sample data file.  Replace the value with your CSV file
leads_file = 'https://raw.githubusercontent.com/eslabsai/salesforce-python/refs/heads/main/leads.csv'

df = pd.read_csv(leads_file)

# convert DataFrame to a list of dictionaries
records = df.to_dict('records')

# traverse through the list and insert into Salesforce
for row in records:
    print(row, "\n")
    result = sf.Lead.create(row)
    if result.get('success'):
        print(result.get('success'))

        