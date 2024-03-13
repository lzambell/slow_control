import urllib.request, json
from datetime import datetime, timedelta
import numpy as np

def access_slow_control(det, from_cern, elemID, day_start, day_stop):
    if(from_cern is True):
        return access_via_cache(det, elemID, day_start, day_stop)
    else:
        return access_via_page(det, elemID, day_start, day_stop)

def access_via_cache(det, elemID, day_start, day_stop):

    """ it's not working for NP04, so temporarily redirecting to the webpage method """
    return access_via_page(det, elemID, day_start, day_stop)    
    
    if(det == 'np02'):
        url = 'http://np02cache.cern.ch:5000/day'
    else:
        url = 'http://epdtdi-vm-01.cern.ch:5000/day/'
        #'http://np04cache.cern.ch:5000/day'
        #

        
    data = []
    day = day_start

    while (day <= day_stop):
        rr = urllib.request.urlopen(url + '/' + day.strftime("%Y-%m-%d") + '/' + str(elemID) ) 
        r = rr.read()
        res = json.loads(r)
        temp = [res[i] for i in range(len(res))]
        for i in range(len(temp)):
            data += temp[i]
            
        day = day + timedelta(days=1)

    data = np.array(data)
    if(len(data) > 0):
        """ converts the timestamps to s """
        data[:,0] *= 1.e-3     

    return data


def access_via_page(det, elemID, day_start, day_stop):

    if(day_start.date() == day_stop.date()):
        day_stop = day_stop + timedelta(days=1)
        

    if(det=='np02'):
        url = 'https://np02-slow-control.web.cern.ch/np02-slow-control/app/php-db-conn/histogramrange.conn.php?'
        url += 'elemId=' + str(elemID)
        url += '&start=' + day_start.strftime("%d-%m-%Y")
        url += '&end=' + day_stop.strftime("%d-%m-%Y")
    else:
        tmp_url = 'https://np04-slow-control.web.cern.ch/np04-slow-control/app/#!/histogram/'
        tmp_url += str(elemID)
        tmp_url += '&start=' + day_start.strftime("%d-%m-%Y")
        tmp_url += '&end=' + day_stop.strftime("%d-%m-%Y")
        #print(tmp_url)
        #
        url = 'https://np04-slow-control.web.cern.ch/np04-slow-control/app/php-db-conn/histogramrange.conn.php?'
        url += 'elemId=' + str(elemID)
        #url += str(elemID)
        url += '&start=' + day_start.strftime("%d-%m-%Y")
        url += '&end=' + day_stop.strftime("%d-%m-%Y")
        #print(url)


    rr = urllib.request.urlopen(url)
    r = rr.read()

    res = json.loads(r)

    data = res['records']
    data = np.array(data)

    """ converts the timestamps to s """
    data[:,0] *= 1.e-3     

    return data

    
