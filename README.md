  CNPC Utils 
=============


fetchParambySO
------

*usage*
python  fetchParambySO.py [service offerring name]

*[input]* 
service offerring name

*[output]* 
csv file, file name  = bp name + timestamp

*howto deploy*
- extract Python27.csm.zip to an windows 2008 64bit box
- add python to env path
- add python/scripts to env path
- modify fetchParambySO, change
gcac = login("http://clm-pm.bmc.local:7070/csm", "CloudAdmin", "password")
to your env.
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