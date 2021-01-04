# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 12:37:07 2020

@author: sega01
"""
import datetime 
#spread in 30 min bins

times=[["2020-10-07T12:00:00.000Z","2020-10-07T13:59:59.999Z"],["2020-10-07T14:00:00.000Z","2020-10-07T16:59:59.999Z"],["2020-10-07T17:00:00.000Z","2020-10-07T18:59:59.999Z"],["2020-10-07T19:00:00.000Z","2020-10-07T21:59:59.999Z"],["2020-10-08T01:00:00.000Z","2020-10-08T06:59:59.999Z"],["2020-10-08T06:00:00.000Z","2020-10-08T09:59:59.999Z"],["2020-09-01T11:00:00.000Z","2020-09-01T16:59:59.999Z"],["2020-09-01T18:00:00.000Z","2020-09-01T20:59:59.999Z"],["2020-09-02T04:00:00.000Z","2020-09-02T09:59:59.999Z"],["2020-09-02T12:00:00.000Z","2020-09-02T16:59:59.999Z"],["2020-09-02T19:00:00.000Z","2020-09-02T22:59:59.999Z"],["2020-09-03T00:00:00.000Z","2020-09-03T06:00:00.000Z"],["2020-08-12T11:06:00.000Z","2020-08-12T11:59:59.999Z"],["2020-08-12T20:00:00.000Z","2020-08-12T23:59:59.999Z"],["2020-08-13T18:00:00.000Z","2020-08-13T21:59:59.999Z"],["2020-08-14T00:00:00.000Z","2020-08-14T06:59:59.999Z"],["2020-08-20T10:30:00.000Z","2020-08-20T15:29:59.999Z"],["2020-08-20T19:30:00.000Z","2020-08-20T23:59:59.999Z"],["2020-08-21T03:00:00.000Z","2020-08-21T08:59:59.999Z"],["2020-08-21T12:00:00.000Z","2020-08-21T17:59:59.999Z"],["2020-08-21T18:00:00.000Z","2020-08-21T21:59:59.999Z"]]
new_times=[]
gap=1800

def to_string(t):
    text = t.isoformat()
    result=text[:(len(text)-3)]+'Z'
    return result

for p in times:
    t_0=datetime.datetime(year=int(p[0][0:4]), month=int(p[0][5:7]), day=int(p[0][8:10]), hour=int(p[0][11:13]),  minute=int(p[0][14:16]), second=0, microsecond=1000)
    t_1=datetime.datetime(year=int(p[1][0:4]), month=int(p[1][5:7]), day=int(p[1][8:10]), hour=int(p[1][11:13]),  minute=int(p[1][14:16]), second=0, microsecond=1000)
    if (t_1-t_0)>datetime.timedelta(seconds=gap):
        not_done=True
        while not_done:
            new_t=t_0+datetime.timedelta(seconds=gap)
            if (t_1-new_t)>datetime.timedelta(seconds=gap):
                new_times.append([to_string(t_0),to_string(new_t)])
                t_0=new_t
            else:
                new_times.append([to_string(t_0),to_string(new_t)])
                new_times.append([to_string(new_t),to_string(t_1)])
                not_done=False
    else:
        new_times.append(p)
            