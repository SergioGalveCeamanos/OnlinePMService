# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 09:44:07 2020

@author: sega01
"""

import requests
from classes.elastic_manager_class import elastic_manager
import pandas as pd
import copy

path=r"\\terfile01\ULTRACOOL\PL\Projects\Shared\LAUDA Cloud\LUC - Industrial PhD\Follow Up\Evaluation MVP\gathered_telemetry.csv"
host='52.169.220.43:9200'
machine=71471
em=elastic_manager(host,machine)
em.connect()
agg_seconds=1

time_bands=[["2020-10-08T02:00:00.001Z", "2020-10-08T04:00:00.001Z"],["2020-10-07T12:30:00.001Z", "2020-10-07T13:00:00.001Z"],["2020-10-07T13:00:00.001Z", "2020-10-07T13:30:00.001Z"]]
from elasticsearch import Elasticsearch
import pandas as pd
import json
import numpy as np
from matplotlib import cm as CM
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def get_index_analytics(date,ty):
    index=ty+date[5:7]+date[0:4]
    return index 

def get_analytics(client,time_start, time_stop, device, names_analysis):
         ty='pm_data_'
         ind=get_index_analytics(time_start,ty) 
         response = client.search(
            index=ind,
            body={
                  "query": {
                    "bool": {
                      # Also: filter, must_not, should
                      "must": [ 
                        {
                          "match": {
                            "device": device
                          }
                        },
                        {
                        "range": {
                        # Timestap format= "2019-12-30T09:25:20.000Z"
                        "timestamp": { 
                        "gt": time_start, # Date Format in Fault Manager: '2019-05-02 08:00:10'
                        "lt": time_stop 
                                     }
                                 }
                        }
                      ],
                      "must_not": [],
                      "should": []
                    }
                  },
                  "from": 0,
                  "size": 100,
                  "sort": [{ "timestamp" : {"order" : "asc"}}],
                  "aggs": {}
                },
            scroll='5m'
         )
         # DATA ARRANGE: each mso will have a dictionary with as many temporal series as in self.names_analysis --> all msos in the list data
         data=[]
         first=True
         for hit in response['hits']['hits']:
             #print(hit)
             if first:
                 first=False
                 n_msos=len(hit['_source'][names_analysis[0]])
                 for i in range(n_msos):
                     new_mso={}
                     for name in names_analysis:
                         field=hit['_source'][name]
                         if name=='timestamp':
                             new_mso[name]=[field]
                         else:
                             new_mso[name]=[field[i]]
                     data.append(new_mso)
             else: 
                 for i in range(n_msos):
                     for name in names_analysis:
                         field=hit['_source'][name]
                         if name=='timestamp':
                             data[i][name].append(field)
                         else:
                             data[i][name].append(field[i])

            
         sc_id=response['_scroll_id']
         more=True
         while more:
             sc=client.scroll(scroll_id=sc_id,scroll='2m') # ,scroll='1m'
             #sc_id=response['_scroll_id']
             if len(sc['hits']['hits'])==0: #|| total>20
                 more=False
             else:
                 for hit in sc['hits']['hits']:
                     if len(hit['_source'][names_analysis[0]])==n_msos:
                         for i in range(n_msos):
                             for name in names_analysis:
                                 field=hit['_source'][name]
                                 if name=='timestamp':
                                     data[i][name].append(field)
                                 else:
                                     data[i][name].append(field[i])
                     else:
                         print('  [!] WARNING: The gathered analysis data might come from different models, two sizes of MSO_SET: '+str(len(hit['_source'][names_analysis[0]]))+', '+str(n_msos)+'  | timestamp: '+hit['_source']['timestamp'])
                    
         return data

device=71471
host='52.169.220.43:9200'
client=Elasticsearch(hosts=[host])
times=time_bands[0]
names_analysis=['models_error', 'low_bounds', 'high_bounds', 'activations', 'confidence','timestamp']
analysis=get_analytics(client,times[0],times[1],device,names_analysis)

#
from fbprophet import Prophet

df=pd.DataFrame(analysis[0])
t_l=[]
e_l=[]
for i in range(df.shape[0]):
    da=df.iloc[i]['timestamp']
    new_da=da[:10]+' '+da[11:19]
    if new_da not in t_l:
        t_l.append(new_da)
        e_l.append(df.iloc[i]['models_error'])
rearrange={'ds':df.loc[:]['timestamp'],'y':df.loc[:]['models_error']}
data=pd.DataFrame(rearrange)
#
m = Prophet()
m.fit(data)
#
future = m.make_future_dataframe(periods=365)
future.tail()
#
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
#
fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)
