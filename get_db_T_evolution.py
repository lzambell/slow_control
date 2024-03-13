import sys
import os
import numpy as np
from datetime import datetime, timedelta, timezone
import socket

#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec


import access
import dump
        
    
def get_dns_domain():
    return socket.getfqdn().split('.', 1)[1]


def check_dates(date, start, stop):
    if( date == "" and (start < 0) and (stop < 0) ):
        print(" >>> One should give either start(+stop) timestamp or a day of interest !")
        need_help()
    elif( len(date)>0 and ((start > 0) or (stop > 0)) ):
        print(" >>> One should give either start(+stop) timestamp or a day of interest !")
        need_help()

    elif(len(date) > 0 and (start <0) and stop < 0):
        ts_start = datetime.strptime(date, "%d-%m-%Y").replace(tzinfo=timezone.utc).timestamp()
        print(ts_start)
        ts_stop = ts_start + 86400
        return date, ts_start, ts_stop
    
    elif(len(date)== 0 and (start >0)):
        date = datetime.fromtimestamp(start).strftime("%d-%m-%Y")
        if(stop < 0):
            stop = start + 86400
        else:
            if (stop < start):
                print(" >>> stop time is earlier than start time ... ")
                need_help()
        return date, start, stop


    
def need_help():
    print("\nUsage: python get_db_ana.py ")
    print(" -start <timestamp in s> ")
    print(" -stop <timestamp in s> (if not provided, stop time in 24h later than start time)")
    print(" -date <DD-MM-YYY> instead of timestamps, for values in a 24h range")    
    print(" -conf <text file with your 'name  ID' correspondance>")
    print(" -out <name of output file if any (options are .dat, .txt, .py, .root)")
    print(" -h print this message")
    sys.exit()

if len(sys.argv) == 1:
	need_help()
else:
    for index, arg in enumerate(sys.argv):
        if arg in ['-h'] :
            need_help()

ts_start  = -1
ts_stop   = -1
config_file = ""
output_file = ""
date = ""

for index, arg in enumerate(sys.argv):
    if arg in ['-start'] and len(sys.argv) > index + 1:
        ts_start = float(sys.argv[index+1])
    elif arg in ['-stop'] and len(sys.argv) > index + 1:
        ts_stop = float(sys.argv[index+1])
    elif arg in ['-conf'] and len(sys.argv) > index + 1:
        config_file = sys.argv[index + 1]
    elif arg in ['-out'] and len(sys.argv) > index + 1:
        output_file = sys.argv[index + 1]
    elif arg in ['-date'] and len(sys.argv) > index + 1:
        date = sys.argv[index + 1]




date, ts_start, ts_stop = check_dates(date, ts_start, ts_stop)


if(os.path.exists(config_file) is False):
    print(" >>> Dictionnary file do not exist !")
    need_help()


dico = {}
with open(config_file) as f:
    for lines in f.readlines():
        lines = lines.rstrip('\n')
        li = lines.split(' ')        

        dico[li[0]] = int(li[1])

#print(dico)                       

day_start = datetime.fromtimestamp(ts_start)
day_stop = datetime.fromtimestamp(ts_stop)

print(day_start,  ' to ', day_stop)

at_cern = ("cern" in get_dns_domain())
det = 'np04'
values = {}


delta_t = [x for x in range(24)]
delta_t = [t*3600 for t in delta_t]



for name, elemID in dico.items():
    print(name)

    day_start = datetime.fromtimestamp(ts_start)
    day_stop = datetime.fromtimestamp(ts_stop)

    data = access.access_slow_control(det, at_cern, elemID, day_start, day_stop)
    
    time_sel = (data[:,0] > ts_start) & (data[:,0] < ts_stop)
    data_sel = data[time_sel]
    data_sel[:,0] -= ts_start
    
    data_interest = []
    for t in delta_t:
        idx = np.searchsorted(data_sel[:,0], t)
        data_interest.append(data_sel[idx])


    data_interest = np.asarray(data_interest)
    data_interest[:,0] += ts_start

    values[name] = data_interest

np.savez('temp_evo_filling/'+date+'.npz', **values)
