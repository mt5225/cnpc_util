#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

# Pyhton  imports
import json
import sys

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


def saveParamToCSV(bp_name, params):
     #get time stamp
    millis = str(int(round(time.time() * 1000)))

    #open output file for writting
    param_file = open(bp_name + "_" + millis + ".csv", "w")
    param_file.write("BP_NAME,PARAM_NAME,PARAM_GUID" + "\n")

    for param in params:
        msg_body = "%s,%s,%s" % (bp_name, param["parametername"], param["guid"])
        print msg_body
        param_file.write(msg_body + "\n")

def getBlueprintBysoName(gcac,so_name):
    # Search blueprintdoc for given blueprint name.
    searchParams = {'name':so_name}
    searchResults = searchCloudObjects(gcac, ServiceOffering().cloudClass, **searchParams)
    
    if searchResults.totalRows:
        soObject = searchResults.results[0]
    else:
        raise CloudSDKException("There is no serviceoffering found with name [%s]" %so_name)

    bpref_guid = soObject.blueprintReference.split('/')[-1]
    searchParams = {'guid': bpref_guid}
    
    searchResults = searchCloudObjects(gcac, BlueprintReference().cloudClass, **searchParams)
    if searchResults.totalRows:
        soObject = searchResults.results[0]
    else:
        raise CloudSDKException("There is no blueprint found ")
    
    bp_guid = searchResults.results[0].blueprint.split('/')[-1]
    log.debug( "", "action", "Found Blueprint guid %s" %bp_guid)
    return bp_guid


if (__name__ == "__main__"):
    so_name = sys.argv[1]

    #login to csm
    gcac = login("http://clm-pm.bmc.local:7070/csm", "CloudAdmin", "password")
    
    # Search blueprintdoc for given blueprint name.
    searchParams = {'blueprint.guid':getBlueprintBysoName(gcac, so_name)}
    searchResults = searchCloudObjects(gcac, BlueprintDocument().cloudClass, **searchParams)
    if searchResults.totalRows:
        blueprintDocumentobj = searchResults.results[0]
        blueprintName = blueprintDocumentobj.name  ## Get Blueprint guid from document object.
        blueprintDocGUID = blueprintDocumentobj.getGuid()
        log.debug("", "action", "Found blueprintDocGUID %s" %blueprintDocGUID) 
    else:
        raise CloudSDKException("There is no blueprint found with name [%s]" %blueprintName)

    #return all params
    blueprintContent = json.loads(blueprintDocumentobj.content)
    params = blueprintContent["configurations"][0]["parameters"]
    saveParamToCSV(blueprintName, params)