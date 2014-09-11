#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

# Pyhton  imports
import json,sys

# Project imports
from com.bmc.cloud.sdk.apiutils.utils import *
from com.bmc.cloud.sdk.configuration.logger import *
from com.bmc.cloud.sdk.client.generated import *
from com.bmc.cloud.sdk.configuration.logger import SDKLogger

#Bean imports
from com.bmc.cloud.model.beans.ServiceOffering import ServiceOffering
from com.bmc.cloud.sdk.exception import CloudSDKException
from com.bmc.cloud.model.beans.BlueprintDocument import BlueprintDocument
from com.bmc.cloud.model.beans.BlueprintReference import BlueprintReference

# get logger 
log = SDKLogger().getLogger("serviceutils")

__CSM_URL__ = "http://clm-pm.bmc.local:7070/csm"
__CSM_USER__ = "CloudAdmin"
__CSM_PASSWD__ = "password"

def saveParamToCSV(bp_name, blueprintDocGUID, versionNumber, params):
     #get time stamp

    #open output file for writting
    param_file = open("%s_v%d_%s.csv" %(bp_name, versionNumber, blueprintDocGUID), "w")
    param_file.write("BP_NAME,PARAM_NAME,PARAM_GUID" + "\n")
    print "[[[%s %s]]]" % (bp_name, blueprintDocGUID)

    for param in params:
        msg_body = "%s,%s,%s" % (bp_name, param["parametername"], param["guid"])
        print msg_body
        param_file.write(msg_body + "\n")

def getBlueprintBysoName(gcac,so_name):
    # Search blueprintref for given service offerring name.
    searchParams = {'name':so_name}
    searchResults = searchCloudObjects(gcac, ServiceOffering().cloudClass, **searchParams)
    
    if searchResults.totalRows:
        soObject = searchResults.results[0]
    else:
        raise CloudSDKException("There is no serviceoffering found with name [%s]" %so_name)

    bpref_guid = soObject.blueprintReference.split('/')[-1]
    searchParams = {'guid': bpref_guid}
    
    # Search blueprint guid for given blueprintref
    searchResults = searchCloudObjects(gcac, BlueprintReference().cloudClass, **searchParams)
    if searchResults.totalRows:
        soObject = searchResults.results[0]
    else:
        raise CloudSDKException("There is no blueprint found ")
    
    # get blueprint guid 
    bp_guid = searchResults.results[0].blueprint.split('/')[-1]
    log.debug( "", "action", "Found Blueprint guid %s" %bp_guid)
    return bp_guid


if (__name__ == "__main__"):
    # read service offerring name from user input
    so_name = sys.argv[1]

    #login to csm
    gcac = login(__CSM_URL__, __CSM_USER__, __CSM_PASSWD__)
    
    # Search blueprintdoc 
    searchParams = {'blueprint.guid':getBlueprintBysoName(gcac, so_name)}
    searchResults = searchCloudObjects(gcac, BlueprintDocument().cloudClass, **searchParams)
    if searchResults.totalRows:
        for blueprintDocumentobj in searchResults.results:
            blueprintName = blueprintDocumentobj.name  
            blueprintDocGUID = blueprintDocumentobj.getGuid()
            log.debug("", "action", "Found blueprintDocGUID %s" %blueprintDocGUID) 
            versionNumber = blueprintDocumentobj.versionNumber
            blueprintContent = json.loads(blueprintDocumentobj.content)
            try :
                params = blueprintContent["configurations"][0]["parameters"]
                saveParamToCSV(blueprintName, blueprintDocGUID, versionNumber, params)
                time.sleep(1)
            except Exception: 
                pass
    else:
        raise CloudSDKException("There is no blueprint found with name [%s]" %blueprintName)

