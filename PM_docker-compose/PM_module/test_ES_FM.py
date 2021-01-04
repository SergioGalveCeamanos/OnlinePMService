# -*- coding: utf-8 -*-
"""
REGRESSION TEST
"""
import tensorflow as tf
import os, requests, uuid, json, pickle
import copy
from classes.fault_detector_class_ES import fault_detector
#from classes.pm_manager import file_location,load_model
from classes.pdf_nn_class import PDF_NN
import numpy as np
import tabulate as tabulate
import itertools
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Funtions to interact with the fault manager
def load_model(filename,model_dir):
    fault_manager = fault_detector(filename=[],mso_txt=[],host=[],machine=[],matrix=[],sensors=[],faults=[],sensors_lookup=[],sensor_eqs=[],preferent=[],filt_value=9,filt_parameter=[],filt_delay_cap=[],main_ca=[],max_ca_jump=[])
    fault_manager.Load(model_dir,filename)
    return fault_manager

def file_location(device,root_path=r'.\models\model_'):
    device=int(device)
    filename = root_path+str(device)+r'\FM_'+str(device)+'.pkl'
    model_dir =root_path+str(device)+'\\'
    return filename, model_dir

#filename="FM_ES_060320.pkl" # the good
#filename="FM_ES_050320.pkl" # the good
device=71471
file, folder = file_location(device)
fm=load_model(file, folder)
test=fm.training_data.head(50000)

mso_set=[0,10,47,65,96,128,132,141]
faults=fm.faults
fault_manager=fm
matrix=fm.str_matrix
###################### TEST PDF NN ############################

        
sensors_in_tables={1:"ControlRegCompAC__VarPowerKwMSK",2:"EbmpapstFan_1_Mng__CurrPowerkWMSK",3:"Data_EVD_Emb_1__EVD__Variables__EEV_PosPercent__Val",4:"PumpPress",8:"WaterFlowMeter",9:"SuctSH_Circ1",10:"DscgTempCirc1",11:"SubCoolTempCir1",13:"EvapTempCirc1",14:"CondTempCirc1",15:"CondOutTempCirc1",17:"W_OutTempUser",18:"W_OutTempEvap",19:"W_InTempUser",21:"FiltPress",24:"PumpPress",25:"ExtTemp"}
names=[]
#for i in sensors_in_tables:
#    names.append(sensors_in_tables[i])
names= ["W_OutTempUser","W_OutTempEvap","W_InTempUser","FiltPress","PumpPress"]  
data=fm.training_data
#data=data.loc[data['UnitStatus'] == '9.0']
for name in list(data.columns):
    if (name not in names):
        data=data.drop([name],axis=1)
data = data.astype(float)
dims=data.shape[1]
acc=[]
for i in range(dims):
    a=(data[names[i]].max()-data[names[i]].min())/40
    acc.append(a)
  
filename='MC_PDF_5D_24_02_20.pkl'
new_MC_sampling=True
if new_MC_sampling:
    pdf=PDF_NN(dims, acc, filename)
    pdf.load_data(data)
    #pdf.create_training_set(120000)
    #pdf.train_nn()
else:
    try:
        filehandler = open(filename, 'rb') 
        pdf = pickle.load(filehandler)
        filehandler.close()
    except Exception as e: 
        print("Error loading objects: "+str(e))
        

def homog_sampling(data,cont_cond,s=50000,uncertainty=[]):
    stats=data.describe()
    if uncertainty==[]:
        for i in cont_cond:
            a=(data[i].max()-data[i].min())/(40*stats.loc['std'][i])
            uncertainty.append(a)
    lat_var=[]
    for i in data.columns:
        if i not in cont_cond:
            lat_var.append(i)
    done=False
    ws=copy.deepcopy(data)
    sets=[]
    first=True
    pd_sets=[]
    while not done:
        #ind=list(ws.index)
        it_done=False
        sets=[]
        while not it_done:
            i=np.random.randint(0,high=ws.shape[0])
            #samp=ind.pop(i)
            q=ws.iloc[i]
            filt_bool=np.array([True]*ws.shape[0])
            for cc in range(len(cont_cond)):
                l=q[cont_cond[cc]]-uncertainty[cc]
                h=q[cont_cond[cc]]+uncertainty[cc]
                filt_bool = filt_bool & np.array(ws[cont_cond[cc]]>l) & np.array(ws[cont_cond[cc]]<h)
            # with filt_bool we have extracted 
            filt_ws=ws[filt_bool]
            #ind=list(set(ind) - set(filt_ws.index))
            ws=ws.drop(filt_ws.index)
            sets.append(filt_ws)
            if ws.shape[0]==0:
                it_done=True
                print('[!] Sample set found from ws with size='+str(len(sets)))
        #once the list has been sorted in sets, we check if there are too many or too few sets        
        if len(pd_sets)>s or first:
            # we will do the previous process again using as ws the average of the samples 
            new_ws={'set_behind':[]}
            new_sets=[]
            for i in cont_cond:
                new_ws[i]=[]
            # after new_ws is initialize we fill it with the means of the new sets created
            for i in range(len(sets)):
                new_ws['set_behind'].append(i)
                st=sets[i]
                for i in cont_cond:
                    new_ws[i].append(st[i].mean())
            ws=pd.DataFrame(new_ws)
            print('[!] New working set:')
            print(ws)
            # rearrange the pd_sets so that the new set_behind points out to the combined subsets from previous iteration
            if not first:
                new_sets=[]
                for i in range(len(sets)):
                    temp_set=[]
                    ff=True
                    for j in range(sets[i].shape[0]):
                        to_add=int(sets[i].iloc[j]['set_behind'])
                        if ff:
                            temp_set=pd_sets[to_add]
                            ff=False
                        else:
                            temp_set=temp_set.append(pd_sets[to_add],ignore_index=True) 
                    new_sets.append(temp_set)
            else:
                new_sets=sets
                first=False
            for x in range(len(uncertainty)):
                uncertainty[x]=uncertainty[x]*1.5
            pd_sets=copy.deepcopy(new_sets)
            print('[!] End new set arrangement --> pd_sets size: '+str(len(pd_sets)))
        # Once the number of sets is smaller than the required samples, we stop the agregation and take on sample from each set. To fill in the remaining samples we get new samples from each set according to their size                                
        if len(pd_sets)<s:
            # we will take one sample from each and the remaining to fill up to s will be extracted according to the cumm count of samples among sets
            print('[R] Inside low set cond final part of process!')
            initial=True
            missing=s-len(pd_sets)
            dic_sets={'index':[],'size':[]}
            tot=0
            for i in range(len(pd_sets)):
                dic_sets['index'].append(i)
                tot=pd_sets[i].shape[0]
                dic_sets['size'].append(tot)
            # we arrange it in a DF to sort and obtain the cummulative function
            df_sizes=pd.DataFrame(dic_sets)
            df_sizes=df_sizes.sort_values(by=['size'],ascending=False)
            df_sizes['size']=df_sizes['size'].cumsum(axis = 0)
            hits=np.round(np.linspace(0,df_sizes['size'].max(),num=missing))
            loc=0
            new_samples=[]
            # we go though the evenly spaced numbers and collect from which
            for i in hits:
                not_yet=True
                #print(' [o] New selected size and hit: '+str(df_sizes.iloc[loc]['size'])+' | '+str(i))
                while not_yet and loc<df_sizes.shape[0]:
                    if df_sizes.iloc[loc]['size']>i:
                        new_samples.append(df_sizes.iloc[loc]['index'])
                        not_yet=False
                    else:
                        loc=loc+1
            # now we count how many elements are there from each pd_sets
            start_count=True
            for i in new_samples:
                if start_count:
                    start_count=False
                    count_hits = {i:new_samples.count(i)}
                else:
                    count_hits[i] = new_samples.count(i)
            # just load in a new var one sample from each set plus the ones listed in count_hits
            for i in range(len(pd_sets)):
                if i in count_hits:
                    si=count_hits[i]+1
                    randoms=list(np.random.randint(low=0, high=pd_sets[i].shape[0], size=(si,)))
                    add=pd_sets[i].iloc[randoms]
                else:
                    randoms=list(np.random.randint(low=0, high=pd_sets[i].shape[0], size=(1,)))
                    add=pd_sets[i].iloc[randoms]  
                if initial:
                    final_samp=add
                    initial=False
                else:
                    final_samp=final_samp.append(add,ignore_index=True)
                    
            done=True
            print(' [R] --> Final subset obtained:')
            print(final_samp)
        first=False
    # we return the    
    return final_samp

#cont_c=['CondTempCirc1','ExtTemp','WaterFlowMeter']
#result_set=homog_sampling(fm.training_data,cont_c,s=8000)

#(data['WaterFlowMeter'].max()-data['WaterFlowMeter'].min())/(40*stats.loc['std']['WaterFlowMeter'])

#pdf.create_training_set(120000)
#normed_test_label,test_predictions=pdf.train_nn()
        

###################### Evaluate Faulty Case ############################

# Code in: Extra_code_1__tf_test_regression.txt

###################### Test Performance ################################
"""data,names=fault_manager.get_data_names(option='CarolusRex',times=[['2019-05-02 08:00:10','2019-05-02 12:01:10']])
data=pd.DataFrame(data)
data=data.loc[data['UnitStatus'] == '9.0']

for name in list(data.columns):
    if (name not in fault_manager.models[46].source) and (name!=fault_manager.models[46].objective):
        data=data.drop([name],axis=1)
data = data.astype(float)

measured=data.pop(fault_manager.models[46].objective)
normalized=fault_manager.models[46].norm(data,fault_manager.models[46].train_stats)
test_predictions = fault_manager.models[46].model.predict(normalized).flatten()
error = test_predictions - measured
x=[]
for i in range(len(measured)):
    x.append(i)

fig, ax = plt.subplots()
ax.hist(error, bins = 25)
plt.xlabel("Prediction Error")
plt.title(("Errors for MSO # "+str(fault_manager.models[46].mso_reduced_index)))
o = plt.ylabel("Count")
plt.show()   
 
fig, ax = plt.subplots()
ax.plot(x[:500],test_predictions[:500],'r',linewidth=0.35)
ax.plot(x[:500],measured[:500],'b',linewidth=0.35)
plt.show() """ 


####################### Save/Load fault manager #######################
"""re_train=True
file_name='fault_manager.pkl'
if re_train:
    
    file = open(file_name, 'wb') 
    pickle.dump(fault_manager, file)
    file.close()
else:
    filehandler = open(file_name, 'rb') 
    fault_manager = pickle.load(filehandler)

for mso in mso_set:
    print("MSO #"+str(mso)+":")
    print("    Variables: "+str(fault_manager.models[mso].variables))
    print("    Measured: "+str(fault_manager.models[mso].known))
    print("    Equations: "+str(fault_manager.models[mso].equations))
    print("    Faults: "+str(fault_manager.models[mso].faults))"""
    
    
####################### New Table Variables-Measured #######################
"""variables=[['']]
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


variables=[['']]
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
print(tabulate.tabulate(data,tablefmt='latex'))


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


plt.bar(plot_Hx.keys(), plot_Hx.values(), color='g')"""
    
    
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



for mso in mso_set:

    #print(("MSO"+str(mso)+"  PCA: "+str(a)+", "+str(b)+"  Errors: "+str(c)+", "+str(d)))
    print(fault_manager.models[mso].objective)
    