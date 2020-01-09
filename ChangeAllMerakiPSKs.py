"""
Copyright (c) 2019 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
# This script retrieves a Meraki MX L3 Firewall rule from the file NewRuleToAdd.txt and adds it to all
# networks in the Org. The rule inserted only specifies the Destination IPs (destCidr field) and uses
# the comment specified in the first line of the input file for the "comment" field of the rule
# all other parameters for the rule are specified in templateRuleDict below for all insertions.

import time
import sys
import config
import requests
import csv

csvinputfile = None
thePSKs={}

import meraki
dashboard = meraki.DashboardAPI(config.meraki_api_key)


#first the PSKs you want to use
fieldnamesin = ['SSID', 'PSK']
with open('PSK.csv', newline='') as csvinputfile:
    datareader = csv.DictReader(csvinputfile, fieldnames=fieldnamesin)
    for row in datareader:
        thePSKs[row['SSID']]=row['PSK']


#check at least one PSK to configure
if len(thePSKs)==0:
    print("Input file must have at least one SSID, PSK pair!")
    sys.exit(1)

#obtain all networks in the Org specified by the config variable
try:
    myNetworks = dashboard.networks.getOrganizationNetworks(config.meraki_org_id)
except meraki.APIError as e:
    print(f'Meraki API error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'some other error: {e}')
    sys.exit(1)

#stop the script if the operator does not agree with the operation being previewed
print("About to update the all the APs PSKs as follows for their corresponding SSID : " )
print(thePSKs)
print("in the following networks:")
for theNetwork in myNetworks:
    theNetworkid = theNetwork["id"]
    theNetworkname = theNetwork["name"]
    print(theNetworkid, "  ",theNetworkname)
if not input("Procced? (y/n): ").lower().strip()[:1] == "y": sys.exit(1)


for theNetwork in myNetworks:
    theNetworkid = theNetwork["id"]
    #comment the 3 lines below if you do not want to filter out networks whose name matches that condition
    if theNetwork["name"].startswith('z') or theNetwork["name"].endswith('switch-wifi') or theNetwork["name"].endswith('camera') or theNetwork["name"].endswith('systems manager'):
        print("Skipping network named: ",theNetwork["name"], " because it starts with z or ends with switch-wifi, camera or systems manager" )
        continue

    print("Updating PSKs for Network ID: "+theNetworkid+" named: ",theNetwork["name"],"...")
    continueAnswer="y"
    #Comment line below if you wish to skip confirmation for each Network
    continueAnswer=input("Continue? yes, no or skip(y/n/s): ").lower().strip()[:1]
    if continueAnswer=="n":
        print("Bye!")
        sys.exit(1)
    elif continueAnswer=="s":
        print("Skipping Network ID: "+theNetworkid+" named: ",theNetwork["name"],"...")
        continue

    #get the SSIDs
    theSSIDList=dashboard.ssids.getNetworkSsids(theNetworkid)

    theSSIDsToUpdate=[]
    for theSSID in theSSIDList:
        if theSSID['authMode']=='psk' and (theSSID['name'] in thePSKs):
            theSSID['psk']=thePSKs[theSSID['name']]
            theSSIDsToUpdate.append(theSSID)

    print("These are the SSIDs I am about to update:")
    print(theSSIDsToUpdate)

    #add back the updated SSID
    for theUpdateSSID in theSSIDsToUpdate:
        theResult=dashboard.ssids.updateNetworkSsid(
                                    networkId=theNetworkid,
                                    number=theUpdateSSID['number'],
                                    name=theUpdateSSID['name'],
                                    enabled=theUpdateSSID['enabled'],
                                    authMode=theUpdateSSID['authMode'],
                                    encryptionMode=theUpdateSSID['encryptionMode'],
                                    psk=theUpdateSSID['psk'])
        #print(theResult)

    #need to make sure we do not send more than 5 API calls per second for this org
    #so sleep 500ms since we are making 2 API calls per loop
    time.sleep(0.5)

print("Done!")
