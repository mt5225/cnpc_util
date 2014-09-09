import sys,json;
from pprint import pprint
import time


if ( __name__ == '__main__' ) :
	
	#open bp exported file
	filename = sys.argv[1]
	with open(filename) as data_file:
		data = json.load(data_file)
	
	#get bp info
	bp_name = data["entries"][0]["name"]
	bp_doc_guid = data["entries"][0]["blueprintDocumentGuid"]
	params = data["entries"][0]["document"]["configurations"][0]["parameters"]

	#get time stamp
	millis = str(int(round(time.time() * 1000)))

	#open output file for writting
	param_file = open(bp_name + "_" + millis + ".csv", "w")
	param_file.write("BP_NAME, BP_DOC_GUID, PARAM_NAME, PARAM_GUID" + "\n")
	
	#print message body to file
	#format: bp_name, bp_doc_guid, param_name, param_guid
	for param in params:
		item = param["parametername"] + "=" + param["guid"]
		msg_body = "%s,%s,%s,%s" % (bp_name,bp_doc_guid, param["parametername"], param["guid"])
		param_file.write(msg_body + "\n")

	param_file.close()
