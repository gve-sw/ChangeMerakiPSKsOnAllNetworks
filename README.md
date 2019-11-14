# Change Meraki MR Pre-Shared Key on all Networks

This is a simple Python script that takes a PSK.csv file as input to change the Pre-Shared Keys (PSK) for the specified
SSIDs for all networks in an organization.
Before going off to make the changes, it will print out to console a summary of the SSIDs and PSKs and the list of all networks it will affect.
It will then ask for confirmation from the operator of the script.


## Dependencies and initial setup:

Python 3.6 with the following modules installed: 

1. requests
2. meraki
3. csv


More details on the meraki module here:
https://github.com/meraki/dashboard-api-python

 
You can typically install those modules with the following commands: 

pip install requests

pip install meraki

The csv library should be included with the Python install package.

You need to have a file named config.py in the same directory as the ChangeAllMerakiPSKs.py
script with the definition of the Meraki API key to use to run the code as well as the Org ID for
the Organanization for which you want to change the rules for all Networks.
You can obtain the Meraki API Key and the org ID by following the instructions here:
https://developer.cisco.com/meraki/api/#/rest/getting-started

Example of content of the **config.py** file you must create: 
``` 
meraki_api_key = "yourMerakiAPIKey"
meraki_org_id = "yourOrgID"
```

You also need to have the input file named PSK.csv in the same directory as the **ChangeAllMerakiPSKs.py**
It is a comma separated file where each row should have the following format:

SSID, PSK


Example of content of the **PSK.csv** file you must create:

``` 
TESTSSID1, thePSKtoUSE
TESTSSID2, thePSKtoUSE
```

## Running the code:

python3 ChangeAllMerakiPSKs.py

You will be prompted for confirmation before proceeding with the overall operation. 
You will also be prompted on a per Network basis if you wish to proceed with adding the rules

If you wish to remove this last confirmation so the script can run for all Networks
without interruption, look for the comment below in the **ChangeAllMerakiPSKs.py**
file and comment the line below it by adding # as the first character of the line

_"#Comment line below if you wish to skip confirmation for each Network"_



