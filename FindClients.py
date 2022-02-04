## Find Client 
## Script Author: Nadeem Rasool
## Usage: python3 FindClient.py 

import requests
import base64
import json
last_id = 0
username = "xxx" ## Application owner client id
password = "xxx" ## Application owner secret
userpass = username + ':' + password
encoded_u = base64.b64encode(userpass.encode()).decode()

while True:
    response = requests.post(     
        'https://customer.eu.janraincapture.com/entity.find',
        headers = {"Authorization" : "Basic %s" % encoded_u},
        data={
            'type_name': 'user',
            'max_results': '100',
            'attributes': '["id","uuid"]',
            'sort_on': '["id"]',
            'filter': "id > {} and clients is not null".format(last_id)
        }
    )


    json_resp = json.loads(response.text)
    if json_resp['stat'] == 'ok' and json_resp.get('result_count', 0) > 0:
        for record in json_resp['results']:
            # do something with record

            client_response = requests.post(
                'https://customer.eu.janraincapture.com/entity.replace',
                headers = {"Authorization" : "Basic %s" % encoded_u},
                data={
                        'type_name': 'user',
                        'uuid': record['uuid'],
                        'attributes': '[]',
                        'attribute_name': 'clients'
                    }
         )
            print(record['uuid'])
            # update last_id variable with last record in the results
            last_id = record['id']
    else:
        # stop iterating when there are no more results
        #print(json.loads(response.text))
        print("All Done!")
        break 