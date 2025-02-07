import urllib.request, json
from datetime import datetime, timedelta
import numpy as np

def access_slow_control(det, from_cern, elemID, day_start, day_stop):
    if(from_cern is True):
        return access_via_cache(det, elemID, day_start, day_stop)
    else:
        return access_via_page(det, elemID, day_start, day_stop)

def access_via_cache(det, elemID, day_start, day_stop):

    """ cache acces is no longer working, so temporarily redirecting to the webpage method """
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
        url = 'https://np02-data-api-slow-control.app.cern.ch/np02histogram/'
        url += str(elemID)
        url += '/'+day_start.strftime("%Y-%m-%d")+"%2000:00:00"
        url += '/'+day_stop.strftime("%Y-%m-%d")+"%2023:59:59"


        rr = urllib.request.urlopen(url)
        r = rr.read().decode("utf-8").strip()#[1:-1]

        res = json.loads(r)

        data = []
        for key, val in res.items():
            data.append([int(key), val])

        data = np.array(data)

        
    elif(det=='np04'):

        url = 'https://np04-slow-control.web.cern.ch/np04-slow-control/app/php-db-conn/histogramrange.conn.php?'
        #url = 'https://np04-slow-control.web.cern.ch/np04-slow-control/app/php-db-conn/np04histogram.php?'
        url += 'elemId=' + str(elemID)
        url += '&start=' + day_start.strftime("%d-%m-%Y")
        url += '&end=' + day_stop.strftime("%d-%m-%Y")

        print(url)

        rr = urllib.request.urlopen(url)
        r = rr.read()

        res = json.loads(r)
        
        data = res['records']
        data = np.array(data)
        
    else:
        print('Cannot access SC data for ',det,' detector\nBye!')
        exit()

    
    if(len(data) == 0):
        return data

        
    """ converts the timestamps to s """
    data[:,0] *= 1.e-3     

    return data

    
