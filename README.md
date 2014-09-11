  CNPC Utils 
=============


fetchParambySO
------

*[intro]*
- given service offerring name, return param guid in all blueprint versions
- output to csv files, named by blueprint_version_guid

*[usage]*
- python  fetchParambySO.py [service offerring name]
- example:  python fetchParambySO.py "Apache - HedHat 5.8"

*[input]* 
- service offerring name

*[output]* 
- csv file, file name  = bp name + timestamp

*howto deploy in windows*
- install python 2.7.8
- extract Python27.csm.zip to an temp folder
- copy folder Lib\site-packages, scripts to python install dir
- add python to env path
- add python/scripts to env path
- modify fetchParambySO, change
__CSM_URL__ = "http://clm-pm.bmc.local:7070/csm"
__CSM_USER__ = "CloudAdmin"
__CSM_PASSWD__ = "password"
  to you clm setting
- enjoy !

=====================line break========================

bp_param_extracter
------

*usage*
python  bp_param_extracter.py [bp export file]

*[input]* 
export json file name

*[output]* 
csv file, file name  = bp name + timestamp