# -*- coding: utf-8 -*-
"""
REGRESSION TEST
"""
import tensorflow as tf

import copy
import numpy as np
import tabulate as tabulate
import itertools
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from classes.fault_detector_class_ES import fault_detector


def load_model(filename,model_dir):
    fault_manager = fault_detector([],[],[],[],[],[],[],[],[],[],[],9,[])
    fault_manager.Load(model_dir,filename)
    return fault_manager

def file_location(device,root_path=r'\\terfile01\ULTRACOOL\PL\Projects\Shared\LAUDA Cloud\LUC - Industrial PhD\Follow Up\Evaluation MVP\vol_230920_AUSUM_VM\model_'):
    device=int(device)
    filename = root_path+str(device)+'/FM_'+str(device)+'.pkl'
    model_dir =root_path+str(device)+'/'
    return filename, model_dir
   
    
device=71471
file, folder = file_location(device)
fault_manager=load_model(file, folder)  
faults=fault_manager.faults
mso_set=fault_manager.mso_set
sensors=fault_manager.sensors_lookup
matrix=fault_manager.str_matrix
####################### New Table Variables-Measured #######################
variables=[['']]
for fau in faults:
    variables[0].append(faults[fau])
data_variables=[]
for mso in mso_set:
    header=variables
    new_line=[("MSO_"+str(mso))]
    for i in faults:
        x=fault_manager.FSSM[i][mso]
        new_line.append(str(round(x, 3)))
    data_variables.append(new_line)
    
data=header+data_variables
print(tabulate.tabulate(data,tablefmt='latex'))


'''variables=[['']]
for fau in sensors:
    variables[0].append(sensors[fau])
data_variables=[]
for mso in mso_set:
    header=variables
    new_line=[("MSO_"+str(mso))]
    for i in sensors:
        x=SM[mso][i]
        new_line.append(str(round(x, 3)))
    data_variables.append(new_line)
    
data=header+data_variables
print(tabulate.tabulate(data,tablefmt='latex'))'''


# given the row var get probability of column variable
variables=[['']]
plot_Hx={}
for fau in sensors:
    variables[0].append(sensors[fau])
data_variables=[]
for v1 in sensors:
    header=variables
    new_line=[(sensors[v1])]
    for v2 in sensors:
        entry1=(fault_manager.sensors_lookup[v1]+'-'+fault_manager.sensors_lookup[v2])
        entry2=(fault_manager.sensors_lookup[v2]+'-'+fault_manager.sensors_lookup[v1])
        if entry1 in fault_manager.entropy:
            x=fault_manager.entropy[entry1]['Hy_p_x']
            plot_Hx[fault_manager.sensors_lookup[v1]]=fault_manager.entropy[entry1]['Hx']
            new_line.append(str(round(x, 3)))
        elif entry2 in fault_manager.entropy:
            x=fault_manager.entropy[entry2]['Hx_p_y']
            plot_Hx[fault_manager.sensors_lookup[v1]]=fault_manager.entropy[entry2]['Hy']
            new_line.append(str(round(x, 3)))
        else:
            new_line.append('X')
    data_variables.append(new_line)
    
data=header+data_variables
print(tabulate.tabulate(data,tablefmt='latex'))


plt.bar(plot_Hx.keys(), plot_Hx.values(), color='g')
    
    
variables=[['','$W_{c}$','$W_{f}$','$V$','$W_{p}$','$Q_{app}$','$m_{r}$','$m_{a}$','$m_{w}$','$T_{r1}$','$T_{r2}$','$T_{r3}$','$T_{r4}$','$P_{r1}$','$P_{r2}$','$P_{r3}$','$P_{r4}$','$T_{w1}$','$T_{w2}$','$T_{w3}$','$T_{w4}$','$P_{w1}$','$P_{w2}$','$P_{w3}$','$P_{w4}$','$T_{a,atm}$','$T_{a,out}$','$P_{a,atm}$']]
data_variables=[]
for mso in mso_set:
    header=variables
    new_line=[("MSO_"+str(mso))]
    for i in range(1,len(variables[0])):
        if i in fault_manager.models[mso].variables:
            if i in fault_manager.models[mso].known:
                new_line.append("m")
            else:
                new_line.append("v")
        else:
            new_line.append(" ")
    data_variables.append(new_line)
    
data=header+data_variables
print(tabulate.tabulate(data,tablefmt='latex'))


eq_header=[]
line=['']
for i in range(len(matrix)):
    line.append(("E"+str(i+1)))
    
eq_header.append(line)

data_variables=[]
for mso in mso_set:
    new_line=[("MSO_"+str(mso))]
    for i in range(1,len(eq_header[0])):
        if i in fault_manager.models[mso].equations:
            new_line.append("x")
        else:
            new_line.append(" ")
    data_variables.append(new_line)
    
data=eq_header+data_variables
print(tabulate.tabulate(data,tablefmt='latex'))


#########
eq_header=[]
line=['']
for f in faults:
    line.append(faults[f])
    
eq_header.append(line)

data_variables=[]
for mso in mso_set:
    new_line=[("MSO_"+str(mso))]
    for f in eq_header[0][1:]:
        if f in fault_manager.models[mso].faults:
            new_line.append("x")
        else:
            new_line.append(" ")
    data_variables.append(new_line)
    
data=eq_header+data_variables
print(tabulate.tabulate(data,tablefmt='latex'))



#for mso in mso_set:

    #print(("MSO"+str(mso)+"  PCA: "+str(a)+", "+str(b)+"  Errors: "+str(c)+", "+str(d)))
    #print(fault_manager.models[mso].objective)
    