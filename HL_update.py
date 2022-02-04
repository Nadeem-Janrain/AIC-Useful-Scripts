## Update API schema to work with HL
## Script Author: Nadeem Rasool
## Usage: python3 HL_update.py -u https://customer.janraincapture.com -t user -i <ApiClientId> -s <ApiClientSecret>

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


    def addAttribute(url,clientid,clientsecret,entitytype,definition):
        
        endpoint = url+"/entityType.addAttribute"
        dataObject = {'type_name' : entitytype, 'attr_def' : definition}

        response  = requests.post(endpoint, headers=headers,  data = dataObject, auth = (clientid,clientsecret))

        return response

    def setAttributeConstraints(url,clientid,clientsecret,entitytype,attribute_name,constraints):
        
        endpoint = url+"/entityType.setAttributeConstraints"
        dataObject = {'type_name' : entitytype, 'attribute_name' : attribute_name, 'constraints' : constraints }

        response  = requests.post(endpoint, headers=headers,  data = dataObject, auth = (clientid,clientsecret))

        return response

    def removeAttribute(url,clientid,clientsecret,entitytype,attribute_name):

        endpoint = url+"/entityType.removeAttribute"
        dataObject = {'type_name' : entitytype, 'attribute_name' : attribute_name}

        response  = requests.post(endpoint, headers=headers,  data = dataObject, auth = (clientid,clientsecret))

        return response

    def addFeature(attribute_name,feature):

        cmd = "apid-cli adaaf "+attribute+" "+attribute_name+" "+args.entity_type+" -c "+args.config_key

        returned_value = os.system(cmd)
        returned_value_string = str(returned_value)
        
        response = attribute+": "+returned_value_string

        return response

    def caseSensitive(attribute_name):

        cmd = "apid-cli adscs "+args.entity_type+" "+attribute+" -c "+args.config_key

        returned_value = os.system(cmd)
        returned_value_string = str(returned_value)
        
        response = attribute+": "+returned_value_string

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

################# ADD  roles ##################
    message = "ADD roles"
    print(message)
    logging.debug(message)

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

    add_RolesResponse = addAttribute(url,clientid,clientsecret,entitytype,jsondef)
    doLogging(add_RolesResponse)
    


################# ADD  legalAcceptances ##################
    message = "ADD legalAcceptances"
    print(message)
    logging.debug(message)

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
        "name": "legalAcceptanceId",
        "type": "string",
        "case-sensitive": False
      },
      {
        "length": 32,
        "name": "clientId",
        "type": "string",
        "case-sensitive": True
      },
      {
        "name": "dateAccepted",
        "type": "dateTime"
      }
    ],
    "name": "legalAcceptances",
    "type": "plural"
    }
   
    jsondef = json.dumps(definition)

    add_legalAcceptancesResponse = addAttribute(url,clientid,clientsecret,entitytype,jsondef)
    doLogging(add_legalAcceptancesResponse)
    

################ ADD  consents ###########################
    message = "ADD consents"
    print(message)
    logging.debug(message)

    definition =   {
    "attr_defs": [
      {
        "attr_defs": [
          {
            "name": "clientId",
            "length": 32,
            "type": "string",
            "description": "Client ID used to modify the consent."
          },
          {
            "name": "context",
            "length": 100,
            "type": "string",
            "description": "Context in which the consent was changed."
          },
          {
            "name": "updated",
            "type": "dateTime",
            "description": "Date and time of the last change to the consent."
          },
          {
            "name": "type",
            "length": 8,
            "type": "string",
            "description": "Type of consent, 'implicit' or 'explicit'."
          },
          {
            "name": "granted",
            "type": "boolean",
            "description": "Whether or not the consent is granted."
          }
        ],
        "name": "share",
        "type": "object"
      },
          {
        "attr_defs": [
          {
            "name": "clientId",
            "length": 32,
            "type": "string",
            "description": "Client ID used to modify the consent."
          },
          {
            "name": "context",
            "length": 100,
            "type": "string",
            "description": "Context in which the consent was changed."
          },
          {
            "name": "updated",
            "type": "dateTime",
            "description": "Date and time of the last change to the consent."
          },
          {
            "name": "type",
            "length": 8,
            "type": "string",
            "description": "Type of consent, 'implicit' or 'explicit'."
          },
          {
            "name": "granted",
            "type": "boolean",
            "description": "Whether or not the consent is granted."
          }
        ],
        "name": "newsletter",
        "type": "object"
      }
    ],
    "name": "consents",
    "type": "object"
  }

    jsondef = json.dumps(definition)

    add_consentsResponse = addAttribute(url,clientid,clientsecret,entitytype,jsondef)
    doLogging(add_consentsResponse)


################ ADD   accountDeleteRequestTime ##################
    message = "ADD accountDeleteRequestTime"
    print(message)
    logging.debug(message)

    definition =   {
    "name": "accountDeleteRequestTime",
    "type": "dateTime"
  }

    jsondef = json.dumps(definition)

    add_accountDeleteRequestTimeResponse = addAttribute(url,clientid,clientsecret,entitytype,jsondef)
    doLogging(add_accountDeleteRequestTimeResponse)  


################ ADD   accountDataRequestTime ##################
    message = "ADD accountDataRequestTime"
    print(message)
    logging.debug(message)

    definition =   {
    "name": "accountDataRequestTime",
    "type": "dateTime"
  }

    jsondef = json.dumps(definition)

    add_accountDataRequestTimeResponse = addAttribute(url,clientid,clientsecret,entitytype,jsondef)
    doLogging(add_accountDataRequestTimeResponse)  

if __name__ == '__main__':
    main()
