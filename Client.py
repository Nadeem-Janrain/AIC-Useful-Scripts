## Client clear out 
## Script Author: Nadeem Rasool
## Usage: python3 Client.py -u https://<customer>.janraincapture.com -t <user> -i <ApiClientId> -s <ApiClientSecret>

import sys
import time
import os
import json
import argparse
import requests
import types
import logging

def main():

    parser = argparse.ArgumentParser(description='Update API schema to work with HL.')
    
    requiredNamed = parser.add_argument_group('required named arguments')

    requiredNamed.add_argument("-u", "--url",  help="request base url",required=True)
    requiredNamed .add_argument("-t", "--entitytypename",  help="target entity type name",required=True)
    requiredNamed .add_argument("-i", "--clientid",  help="client id",required=True)
    requiredNamed .add_argument("-s", "--clientsecret",  help="client secret",required=True)

    args = parser.parse_args()

    clientsecret = args.clientsecret
    clientid = args.clientid
    url = args.url
    entitytype = args.entitytypename
    #configkey = args.configkey
   
    logging.basicConfig(filename='HL_update.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

    headers = {
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
    def entityFind(url,clientid,clientsecret,entitytype,definition,myfilter):
        
        endpoint = url+"/entity.find"
        dataObject = {'type_name' : entitytype, myfilter }

        response  = requests.post(endpoint, headers=headers,  data = myfilter, auth = (clientid,clientsecret))

        return response
    def doLogging(APIResponse):

        JSONResponse = APIResponse.json()
        stat = JSONResponse["stat"]
        text = APIResponse.text
        httpstat = APIResponse.ok

        if ((httpstat == True) and (stat == "ok")):
            print("stat : "+stat)
        else:
            print(text)
            
        logging.debug(text)

################# Find Clients with data ##################
    message = "Find Clients with data"
    print(message)
    logging.debug(message)

    myfilter = "clients is not null"

    definition =          {
    "attr_defs": [
      {
        "length": 1000,
        "constraints": [
          "locally-unique",
          "required"
        ],
        "features": [
          "primary-key"
        ],
        "name": "display",
        "type": "string",
        "case-sensitive": True
      },
      {
        "length": 256,
        "name": "value",
        "type": "string",
        "case-sensitive": True
     }
    ],
    "name": "roles",
    "type": "plural"
    }
   
    jsondef = json.dumps(definition)

    find_Clients = entityFind(url,clientid,clientsecret,entitytype,myfilter)
    doLogging(find_Clients)