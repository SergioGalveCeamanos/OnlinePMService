# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 13:54:55 2020

@author: sega01
"""

#Repair wrong values

from elasticsearch import Elasticsearch
import pandas as pd
import json

from elasticsearch import Elasticsearch
import pandas as pd
import json
from os import listdir
import pickle
import time
import datetime
import traceback

root=r"\\terfile01\ULTRACOOL\PL\Projects\Shared\LAUDA Cloud\DataCollection"
file_names='\Data_' # and then the date
save_done=r"\\terfile01\ULTRACOOL\PL\Projects\Shared\LAUDA Cloud\DataCollection\Tasks_repaired.pkl"
host='52.169.220.43:9200'
device="71471"
agg=1
last_record="2020-09-03T06:00:30.000Z"
lr="2020-09-03T06_00"
def create_index(data):
    ind='telemetry_'+data['timestamp'][5:7]+data['timestamp'][0:4]
    id_es=data['deviceId']+'_'+data['param']+'_'+data['timestamp']
    return ind, id_es

def delete_telemetry(data,em): 
    ind , id_es=create_index(data)
    try:
        response=em.delete(index=ind,id=id_es,doc_type='telemetry')
        response=False
    except:
        traceback.print_exc()
        response=True
    return response
    
def upload_telemetry(data,em):
    try:
        ind , id_es=create_index(data)
        b=json.dumps(data)
        response=em.create(index=ind,id=id_es,body=b,doc_type='telemetry')
        response=False
    except:
        traceback.print_exc()
        response=True
    return response

def get_tasks():
    t_files=listdir(root)
    filehandler = open(save_done, 'rb') 
    status = pickle.load(filehandler)
    tasks=status.keys()
    filehandler.close()
    for t in t_files:
        if (t[:5]==file_names[1:]):
            if t not in tasks:
                status[t]=0 #to do
            if t[5:21]<lr:
                status[t]=2
    reupload=False
    to_delete=[]
    for t in tasks:
        if t not in t_files:
            to_delete.append(t)
            reupload=True
    if reupload:
        for t in to_delete:
            del status[t]
        filehandler = open(save_done, 'wb')
        pickle.dump(status, filehandler)
        filehandler.close()
    return status
 
def update_tasks(new,state):    
    filehandler = open(save_done, 'rb')
    tasks = pickle.load(filehandler)
    filehandler.close()
    tasks[new]=state
    filehandler = open(save_done, 'wb')
    pickle.dump(tasks, filehandler)
    filehandler.close()

sle=30
template={
"deviceId": device,
"param": "EvapTempCirc1",
"aggregationSeconds": agg,
"timestamp": "2019-02-11T23:00:00.000Z",
"max": 8.75,
"min": 8.73,
"avg": 8.74,
"stddev": 0,
"count": 1
}
max_cod=65536
variables=["SubCoolCir1","EvapTempCirc1"]
repeated=0
while True:
    tasks=get_tasks()
    print(tasks)
    not_found=True
    for name in tasks:
        if not_found and tasks[name]==0:
            not_found=False
            update_tasks(name,1) # on going
            task=name
    path=root+file_names+task[5:]
    db=pd.read_csv(path,index_col=0)
    names=db.columns
    print(' START OF FILE: '+task)
    for index, row in db.iterrows():
        t_a=datetime.datetime.now()
        if row["timestamp"]>last_record:
            em=Elasticsearch(hosts=[host])
            for name in variables:
                if row[name]>(max_cod/2):
                    not_done=True
                    not_deleted=True
                    while not_done or not_deleted:
                        template["param"]=name
                        template["avg"]=-(max_cod-row[name])/10
                        template["min"]=-(max_cod-row[name])/10
                        template["max"]=-(max_cod-row[name])/10
                        template["timestamp"]=row["timestamp"]
                        if not_deleted:
                            not_deleted=delete_telemetry(row["timestamp"],em)
                        if not_done:
                            not_done=upload_telemetry(template,em)
                        if not_done or not_deleted:
                            repeated=repeated+1
                            em=Elasticsearch(hosts=[host])
                            print('  [!] ')
                            if repeated>2:
                                not_done=False
                                not_deleted=False
                                repeated=0
        t_b=datetime.datetime.now()
        dif=t_b-t_a
        #print(' [T] ---> '+str(dif))
    update_tasks(task,2)
    print('[+] Added to ES the documents from file: '+task)
    time.sleep(sle)
            
            
            
