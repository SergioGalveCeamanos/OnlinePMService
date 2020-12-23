# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 09:50:39 2020

@author: sega01
"""


# THINGS TO INCLUDE IN DOCKER PM:
#   - probability and prognosis calculation
#   - devices available

# THINGS TO INCLUDE IN DOCKER ES:
#   - Store data in ES
#   - retrieve analysis data

# THINGS TO INCLUDE IN fault_detector:
#   - prognosis calculation
#   - probability adjustment

import requests
import datetime 
import time

ip='http://0.0.0.0:5000/'
# this must be triggered every X time, parametrized ... by default it is understood that is from now 
# the length sets how much time to go back from time
def launch_all(ip='http://40.85.118.85:5000/',length=datetime.timedelta(hours=1),time="now",devices=['71471']):
    if devices!=['71471']:
        try:
            # headers=headers
            address=ip+'get-devices'
            
            r = requests.get(address) # 'http://db_manager:5001/collect-data'
            data=r.json()
            devices=data['available_models']
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
    
    # date format objective: "2019-12-12T05:45:00.000Z"
    if time=="now":
        now = datetime.datetime.now()#-datetime.timedelta(hours=24)
        end = now.isoformat() # '2020-05-11T09:46:24.878629' ... we must adapt it
    else:
        now = time
        end = time.isoformat()
    start = (now-length).isoformat()
    end=end[:(len(end)-3)]+'Z'
    start=start[:(len(start)-3)]+'Z'
    #print(start)
    #print(end)
    # device per device ... 2 step requests
    data={}
    #print('Available Devices:')
    #print(devices)
    for d in devices:
        address=ip+'re-do-forecast'
        body={"device": int(d),"time_start":start,"time_stop":end}
        r = requests.post(address, json=body, timeout = 3600)
        # It must contain the prediction and also the boundaries
        
    return r

wait=1800
i=-1
while True and i<7:
    i=i+1
    tt=i*wait
    new=datetime.datetime(year=2020, month=9, day=2, hour=11,  minute=40, second=0, microsecond=1000)+datetime.timedelta(seconds=tt)
    data=launch_all(length=datetime.timedelta(seconds=wait),time=new)
    #print(data)
    time.sleep(wait/3)
    

"""payload = ''
headers = {}
conn = http.client.HTTPSConnection("40.115.110.60", 5000)
conn.request("GET", "/get-devices", payload, headers)
res = conn.getresponse()
coded = res.read()  
data=coded.decode("utf-8")"""
        