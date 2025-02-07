import sys
import os
import numpy as np
from datetime import datetime, timedelta
import socket
import imp
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from importlib import import_module
import access
import dump
        
    
def get_dns_domain():
    return socket.getfqdn().split('.', 1)[1]


def check_dates(start, stop):
    if( (start < 0) or (stop < 0) ):
        print(" >>> One should give run start and stop timestamps !")
        need_help()
    elif (stop < start):
        print(" >>> stop time is earlier than start time ... ")
        need_help()

def need_help():
    print("\nUsage: python get_db_ana.py ")
    print("-det np02 or np04")
    print(" -start <timestamp in s> ")
    print(" -stop <timestamp in s> (if not provided, stop time in 24h later than start time)")
    print(" -conf <python dictionnary with your name<->ID correspondance>")
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
detector = ""

for index, arg in enumerate(sys.argv):
    if arg in ['-det'] and len(sys.argv) > index + 1:
        detector = sys.argv[index+1]
    elif arg in ['-start'] and len(sys.argv) > index + 1:
        ts_start = float(sys.argv[index+1])
    elif arg in ['-stop'] and len(sys.argv) > index + 1:
        ts_stop = float(sys.argv[index+1])
    elif arg in ['-conf'] and len(sys.argv) > index + 1:
        config_file = sys.argv[index + 1]
    elif arg in ['-out'] and len(sys.argv) > index + 1:
        output_file = sys.argv[index + 1]



if(len(detector) == 0):
    print('No detector provided!')
    need_help()

if(ts_start > 0 and ts_stop < 0):
    ts_stop = ts_start + 86400 -1

check_dates(ts_start, ts_stop)
if(os.path.exists(config_file) is False):
    print(" >>> Dictionnary file do not exist !")
    need_help()



dico = {}
with open(config_file) as f:
    for lines in f.readlines()[1:-1]:
        lines = lines.rstrip('\n')
        li = lines.split('\t')        

        dico[li[0]] = int(li[1])

#print(dico)                       

day_start = datetime.fromtimestamp(ts_start)
day_stop = datetime.fromtimestamp(ts_stop)

at_cern = ("cern" in get_dns_domain())

values = {}

for name, elemID in dico.items():
    print(name)

    day_start = datetime.fromtimestamp(ts_start)
    day_stop = datetime.fromtimestamp(ts_stop)

    data = access.access_slow_control(detector, at_cern, elemID, day_start, day_stop)
    
    """ set a 5 days cut as it can run forever"""
    count = 0
    while(len(data) == 0 and count < 5):
        day_start = day_start + timedelta(days=-1)
        data = access.access_slow_control(det, at_cern, elemID, day_start, day_stop)
        count += 1
    if(len(data) == 0):
        values[name] = data_sel
        continue

    bef_meas = np.where(data[:,0] < ts_start)

    """ if no points taken before the run"""
    count = 0
    while(len(bef_meas[0]) == 0 and count < 5):
        day_start = day_start + timedelta(days=-1)
        data = access.access_slow_control(det, at_cern, elemID, day_start, day_stop)
        bef_meas = np.where(data[:,0] < ts_start)
        count += 1

    aft_meas   = np.where(data[:,0] > ts_stop)

    """ if no points taken after the run"""
    count = 0
    while(len(aft_meas[0]) == 0 and count < 5):
        day_stop = day_stop + timedelta(days=1)
        data = access.access_slow_control(det, at_cern, elemID, day_start, day_stop)
        aft_meas = np.where(data[:,0] > ts_stop)
        count += 1

    time_sel = (data[:,0] > ts_start) & (data[:,0] < ts_stop)
    data_sel = data[time_sel]
    data_sel[:,0] -= ts_start
    values[name] = data_sel



""" do your thing now :) """

for (name, val) in values.items():
    print(name, ' ->', val[-1])
