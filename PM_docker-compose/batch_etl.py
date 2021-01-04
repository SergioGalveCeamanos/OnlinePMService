# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:40:39 2020

@author: sega01

Batch Script to ask for new evaluation of samples
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
def launch_all(ip='http://15.188.14.252:5000/',length=datetime.timedelta(hours=1),time="now",devices=['71471'],version="_test_3A_201222"):
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
        address=ip+'get-analysis'
        #'get-analysis'
        #'re-do-forecast'
        #'re-do-probabilities'
        print('[!] New Message sent: ')
        body={"device": int(d),"time_start":start,"time_stop":end,"version":version}
        print(body)
        r = requests.post(address, json=body, timeout = 3600)
        # It must contain the prediction and also the boundaries
        
    return r

wait=1800
i=-1
j=-1
follow=True
dates=[["2020-10-07T12:00:00.000Z","2020-10-07T12:30:00.000Z"], # Good Behaviour
       ["2020-10-07T15:00:00.000Z","2020-10-07T15:30:00.000Z"], # Good Behaviour
       ["2020-10-07T22:00:00.000Z","2020-10-07T22:30:00.000Z"], # Good Behaviour
       ["2020-10-08T08:00:00.000Z","2020-10-08T08:30:00.000Z"], # Good Behaviour
       ["2020-10-08T09:00:00.000Z","2020-10-08T09:30:00.000Z"], # Good Behaviour
       ["2020-10-08T10:30:00.000Z","2020-10-08T11:00:00.000Z"], # Bad Behaviour
       ["2020-10-08T12:00:00.000Z","2020-10-08T12:30:00.000Z"], # Bad Behaviour
       ["2020-10-08T13:00:00.000Z","2020-10-08T13:30:00.000Z"], # Bad Behaviour
       ["2020-10-09T13:00:00.000Z","2020-10-09T13:30:00.000Z"], # Bad Behaviour
       ["2020-11-04T12:00:00.000Z","2020-11-04T12:30:00.000Z"], # Good Behaviour
       ["2020-11-04T16:00:00.000Z","2020-11-04T16:30:00.000Z"], # Good Behaviour
       ["2020-11-05T04:00:00.000Z","2020-11-05T04:30:00.000Z"], # Good Behaviour
       ["2020-11-05T05:00:00.000Z","2020-11-05T05:30:00.000Z"], # Good Behaviour
       ["2020-11-05T06:00:00.000Z","2020-11-05T06:30:00.000Z"], # Good Behaviour
       ["2020-11-05T09:00:00.000Z","2020-11-05T09:30:00.000Z"], # Good Behaviour
       ["2020-11-06T10:00:00.000Z","2020-11-06T10:30:00.000Z"], # Bad Behaviour
       ["2020-11-06T12:00:00.000Z","2020-11-06T12:30:00.000Z"], # Bad Behaviour
       ["2020-11-06T13:00:00.000Z","2020-11-06T13:30:00.000Z"], # Bad Behaviour
       ["2020-11-10T17:00:00.000Z","2020-11-10T17:30:00.000Z"]] # Bad Behaviour

for pair in dates:
    i=pair[1]
    new=datetime.datetime(year=int(i[:4]), month=int(i[5:7]), day=int(i[8:10]), hour=int(i[11:13]),  minute=int(i[14:16]), second=0, microsecond=1000)
    data=launch_all(length=datetime.timedelta(seconds=1800),time=new)
    
    
i=-1  
#limit_1=datetime.datetime(year=2020, month=9, day=4, hour=10,  minute=30, second=0, microsecond=1000)
#limit_1=datetime.datetime(year=2020, month=9, day=2, hour=8,  minute=0, second=0, microsecond=1000)
limit_1=datetime.datetime(year=2020, month=9, day=2, hour=22,  minute=30, second=0, microsecond=1000)
while follow:
    i=i+1
    tt=i*wait
    #new=datetime.datetime(year=2020, month=9, day=4, hour=7,  minute=00, second=0, microsecond=1000)+datetime.timedelta(seconds=tt)
    #new=datetime.datetime(year=2020, month=9, day=1, hour=22,  minute=00, second=0, microsecond=1000)+datetime.timedelta(seconds=tt)
    new=datetime.datetime(year=2020, month=9, day=2, hour=16,  minute=0, second=0, microsecond=1000)+datetime.timedelta(seconds=tt)
    if new>=limit_1:
        follow=False
    data=launch_all(length=datetime.timedelta(seconds=wait),time=new)
    #print(data)
    #time.sleep(wait*3)
    

"""payload = ''
headers = {}
conn = http.client.HTTPSConnection("40.115.110.60", 5000)
conn.request("GET", "/get-devices", payload, headers)
res = conn.getresponse()
coded = res.read()  
data=coded.decode("utf-8")"""

'''
import pandas as pd     
file='/models/tasks.csv' 
task={}
task['device']=[]
task['time_start']=[]
task['time_stop']=[]
task['date']=[]
task['status']=[]
task['type']=[]
task['version']=[]
df=pd.DataFrame(task)
df.to_csv(file)
'''
def get_index_analytics(date,ty):
         index=ty+date[5:7]+date[0:4]
         return index 
     
def get_ids(date,ty,sn):
         index=ty+sn+'_'+date
         return index 
if True:
     from elasticsearch import Elasticsearch, helpers
     import pandas as pd
     import json
     import traceback
     data=to_write
     host='52.169.220.43:9200'
     device=71471
     client=Elasticsearch(hosts=[host])
     ty='pm_data_'
     response=True
     ind=get_index_analytics(data[0]['timestamp'],ty)
     for d in range(len(data)):
         data[d]['_id']=get_ids(data[d]['timestamp'],ty,str(data[d]['device']))
     #b=json.dumps(data)
     try:
         resp=helpers.parallel_bulk(client, data, index=ind,doc_type='diagnosis')
     except:
         response=False
         print(' [!] Error uploading forecast')
         traceback.print_exc()
        
for mso in fm.mso_set:
    print(" [*] MSO #"+str(mso))
    print(" --> Variables used:")
    print(fm.models[mso].source)
    print(" --> Variables predicted:")
    print(fm.models[mso].objective)