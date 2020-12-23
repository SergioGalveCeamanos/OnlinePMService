# -*- coding: utf-8 -*-
"""
REGRESSION TEST
"""
import tensorflow as tf
import os, requests, uuid, json, pickle
import copy
from classes.fault_detector_class_ES import fault_detector
#from classes.pdf_nn_class import PDF_NN
import numpy as np
import tabulate as tabulate
import itertools
import pickle
import pandas as pd
import matplotlib.pyplot as plt


new=False

#filename="FM_ES_060320.pkl" # the good
#filename="FM_ES_050320.pkl" # the good
filename="FM_ES_v_forecast.pkl" # the bad
if new:

    machine="69823"
    host='52.169.220.43:9200'
    matrix= [   [1,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0], # Component Eq
                [1,0,0,0,1,1,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                [1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                [0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,1,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                [0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
                [1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],# Mass Eq
                [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0], # Pressure Eq
                [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1], # Direct relation betweeen variables 
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Sensor Eq
                [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]]
    
    # OJO SENSORES: Power of Pump (with total power?), SuctSH_Circ1 (need to add other value?), FiltPress
    # 4:"PumpPress"
    sensors_in_tables={1:"ControlRegCompAC.VarPowerKwMSK",2:"EbmpapstFan_1_Mng.ElectrInfo_EBM_1.CurrPower",3:"Data_EVD_Emb_1.EVD.Variables.EEV_PosPercent.Val",8:"WaterFlowMeter",9:"SuctSH_Circ1",10:"DscgTempCirc1",11:"SubCoolTempCir1",13:"EvapTempCirc1",14:"CondTempCirc1",17:"W_OutTempUser",18:"W_OutTempEvap",19:"W_InTempUser",21:"FiltPress",24:"PumpPress",25:"ExtTemp"}
    sensors={1:"wc",2:"wf",3:"v",4:"wp",8:"mw",9:"tr1",10:"tr2",11:"tr3",13:"pr1",14:"pr2",15:"pr3",17:"tw1",18:"tw2",19:"tw3",21:"pw1",24:"pw4",25:"tatm"}
    faults={1:"fc1",2:"fc2",4:"fc3",5:"fc4",7:"fc5",9:"fl1",10:"fl2",11:"fo1",12:"fo2",13:"fo3",14:"fo4",15:"fo5",22:"fs1",23:"fs2",24:"fs3",25:"fs4",26:"fs5",27:"fs6",28:"fs7",29:"fs8",30:"fs9",31:"fs10",32:"fs11",33:"fs12",34:"fs13"}
    sensor_eqs={"wc":18,"wf":19,"v":20,"wp":21,"mw":22,"tr1":23,"tr2":24,"tr3":25,"pr1":26,"pr2":27,"pr3":28,"tw1":29,"tw2":30,"tw3":31,"pw1":32,"pw4":33,"tatm":34}
    mso_set=[17,15,2,29,32,3,73]
    mso_path= r"C:\Users\sega01\Desktop\Temporal Files\LUC - Industrial PhD\Online Service\PM_docker-compose\PM_module\classes\msos.txt"
    preferent= ["SuctSH_Circ1","DscgTempCirc1","SubCoolTempCir1","W_OutTempUser","W_OutTempEvap","W_InTempUser"]
    times_b=[["2019-12-10T05:45:00.000Z","2019-12-10T19:00:00.000Z"],["2019-12-09T05:45:00.000Z","2019-12-09T19:00:00.000Z"],["2019-10-29T05:45:00.000Z","2019-10-29T19:00:00.000Z"],["2019-10-28T05:45:00.000Z","2019-10-28T19:00:00.000Z"],["2019-10-21T05:45:00.000Z","2019-10-21T19:00:00.000Z"],["2019-10-10T05:45:00.000Z","2019-10-10T19:00:00.000Z"],["2019-10-08T05:45:00.000Z","2019-10-08T19:00:00.000Z"],["2019-10-02T05:45:00.000Z","2019-10-02T19:00:00.000Z"],["2019-10-03T05:45:00.000Z","2019-10-03T19:00:00.000Z"],["2019-10-01T05:45:00.000Z","2019-10-01T19:00:00.000Z"],["2019-09-30T05:45:00.000Z","2019-09-30T19:00:00.000Z"],["2019-11-08T05:45:00.000Z","2019-11-08T19:00:00.000Z"],["2019-11-04T05:45:00.000Z","2019-11-04T19:00:00.000Z"],["2019-11-05T05:45:00.000Z","2019-11-05T19:00:00.000Z"],["2019-09-18T05:25:20.000Z","2019-09-18T19:25:20.000Z"],["2019-09-23T05:25:20.000Z","2019-09-23T19:25:20.000Z"],["2020-01-09T05:45:00.000Z","2020-01-09T17:00:00.000Z"],["2020-01-10T05:45:00.000Z","2020-01-10T15:00:00.000Z"],["2020-01-13T05:45:00.000Z","2020-01-13T18:00:00.000Z"],["2020-01-14T05:45:00.000Z","2020-01-14T18:00:00.000Z"]]
    
    fault_manager = fault_detector(filename,mso_path,host,machine,matrix,sensors_in_tables,faults,mso_set,sensors,sensor_eqs,preferent)
    fault_manager.read_msos()
    fault_manager.MSO_residuals()
    
    mso=17
    
    filename="FM_ES_v_forecast.pkl"
    filehandler = open('test_training_data.pkl', 'rb') 
    training_data = pickle.load(filehandler)
    filehandler.close()
    
    variables=fault_manager.models[mso].known
    names=fault_manager.get_sensor_names(variables)
    goal=names[1]
    names.remove(names[1])
    source=names
    variables=fault_manager.models[mso].known
    names=fault_manager.get_sensor_names(variables)
    i=-1
    y=0
    for name in names:
        i=i+1
        if name in fault_manager.preferent:
            y=i
    goal=names[y]
    names.remove(names[y])
    source=names
    #pass the objective based on the causal map
    predictor='NN'
    outlayers='No'
    option2='default'
    fault_manager.models[mso].train(training_data,source,goal,predictor,option2)
    file = open(filename, 'wb')
    fault_manager.models[mso].save('./Test_FM_Brown/')
    pickle.dump(fault_manager, file)
    file.close()
    
else:
    try:
        filehandler = open('test_training_data.pkl', 'rb') 
        training_data = pickle.load(filehandler)
        training_data=training_data.loc[training_data['UnitStatus'] == 9]
        filehandler.close()
        filehandler = open(filename, 'rb') 
        fault_manager = pickle.load(filehandler)
        fault_manager.models[17].load('./Test_FM_Brown/')
        filehandler.close()
        
        
        #SM=fault_manager.create_SM(samples=1000)
        #fault_manager.load_entropy()
        #fault_manager.create_FSSM(SM)

        
    except Exception as e: 
        print("Error loading objects: "+str(e))

test=training_data.head(5000)

data=test.loc[test['UnitStatus'] == 9]
noise=[]
for i in range(len(data)):
    noise.append(np.random.normal(0.2*fault_manager.models[17].train_stats.loc['SubCoolTempCir1','mean']*i/len(data),fault_manager.models[17].train_stats.loc['SubCoolTempCir1','std']/50))
data = data.drop(['timestamp'],axis=1)
data = data.astype(float)
data["SubCoolTempCir1"]=data["SubCoolTempCir1"]+noise

X=fault_manager.models[17].predict(data)
Ew,f,alpha=fault_manager.forecast_Brown(X.values,1000)
#data_eval=fault_manager.models[one_mso].evaluate_performance(data,option1='NN',option2='PCA')
#fault_manager.evaluate_data([['2019-07-15 06:00:10','2019-07-15 12:01:10']],manual_data=data,option='PCA')
#prior_evo=fault_manager.identify_faults(data)
#fault_manager.plot_prior_evo(prior_evo)
#prior_evolution=fault_manager.prior_update(prior_evo[1], prior_evo[2])
#fault_manager.plot_prior_evo(prior_evolution)


###################### TEST PDF NN ############################

        
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
    
    
"""variables=[['','$W_{c}$','$W_{f}$','$V$','$W_{p}$','$Q_{app}$','$m_{r}$','$m_{a}$','$m_{w}$','$T_{r1}$','$T_{r2}$','$T_{r3}$','$T_{r4}$','$P_{r1}$','$P_{r2}$','$P_{r3}$','$P_{r4}$','$T_{w1}$','$T_{w2}$','$T_{w3}$','$T_{w4}$','$P_{w1}$','$P_{w2}$','$P_{w3}$','$P_{w4}$','$T_{a,atm}$','$T_{a,out}$','$P_{a,atm}$']]
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
    print(fault_manager.models[mso].objective)"""
    