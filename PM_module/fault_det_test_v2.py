# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 12:15:04 2019

@author: sega01
"""

import copy
from DB_management.fault_detector_class_ES import fault_detector
import numpy as np
import itertools

machine="71479"
filename="FM_ES_050320.pkl"
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
mso_set=[17,0,15,2,29,32,3,73]
mso_path= r"\\terfile01\ULTRACOOL\PL\Projects\Shared\LAUDA Cloud\LUC - Industrial PhD\Elastic Cloud\msos.txt"
preferent= ["SuctSH_Circ1","DscgTempCirc1","SubCoolTempCir1","W_OutTempUser","W_OutTempEvap","W_InTempUser"]

fault_manager = fault_detector(filename,mso_path,host,machine,matrix,sensors_in_tables,faults,mso_set,sensors,sensor_eqs,preferent)
fault_manager.read_msos()
fault_manager.MSO_residuals()

##################### MARKING #######################################

repeated=0
combos=[]
for mso in fault_manager.models:
    if mso.faults not in combos:
        combos.append(mso.faults)
        
    else:
        repeated=repeated+1
    
fault_activations=[]
n=-1
for fault in faults:
    i=0
    n=n+1
    fault_activations.append([])
    for mix in combos:
        i=i+1
        if faults[fault] in mix:
            fault_activations[n].append(i)
            
##################### MARKING #######################################
def get_reward(eq_set,fault_manager):
    used_msos=[]
    used_variables=[]
    for mso in eq_set:
        if mso not in used_msos:
            used_msos.append(mso)
            for variable in fault_manager.models[mso].known:
                if variable not in used_variables:
                    used_variables.append(variable)
                
    result=10*(len(used_variables))/len(used_msos)
    return result


# OBSOLETE !!!!!!!!!!!
def compare_activation(f1,f2):
    equal=True
    for mso in f1:
        if mso not in f2:
            equal=False
            
    if equal and (len(f1)!=len(f2)):
        equal=False
            
    return equal

# OBSOLETE !!!!!!!!!!!
#from a set of mso identify the activation of each fault
def mso_set_activation(min_set,fault_manager):
    fault_activations=[]
    n=-1
    for fault in fault_manager.faults:
        i=0
        n=n+1
        fault_activations.append([])
        for m in min_set:
            i=i+1
            if fault_manager.faults[fault] in fault_manager.combos[m]:
                fault_activations[n].append(m) 
                
    return fault_activations

# OBSOLETE !!!!!!!!!!!
#with this function the objective is to get the mso_set proposed and see if all the faults get to be distinguished one from another
def detectable_set(min_set,fault_manager,marks):
    mso_set=mso_set_activation(min_set,fault_manager)
    detectable=True
    n=-1
    #set all marks but the initial marking to -1 ... then change those needed to 0
    for mark in marks:
        n=n+1
        if mark>=0:
            if abs(mark)>0:
                marks[n]=abs(marks[n])
            else:
                marks[n]=-1
    for n in range(len(mso_set)):
        if marks[n]!=[-2]:
            if mso_set[n]==[]:
                detectable=False
            if n<len(mso_set)-1:
                for k in range((n+1),len(mso_set)):
                    if compare_activation(mso_set[n],mso_set[k]):
                        if not (marks[n]==marks[k] and marks[n]<-2):
                            detectable=False
                            marks[n]=0
                            if marks[k]!=[-2]:
                                marks[k]=0
                
    return marks

# OBSOLETE !!!!!!!!!!!
def get_combinations(mso_set,fault_manager):
    combinations=list(itertools.product(mso_set[:]))
    result=copy.deepcopy(combinations)
    for element in combinations:
        i=0
        not_repeated=True
        while not_repeated and i<len(element):
            repeated=element.count(element[i])
            i=i+1
            if repeated>1:
                result.remove(element)
    return result
  

#evaluate how good a new mso is based on the number of appearances, the reward and the difference in the marking (Y-X) to see how relevant it is
def get_score(Y,appearances,fault_manager,mso_set):
    reward=get_reward(mso_set,fault_manager)
    app= 1/(appearances+10)
    i=-1
    news=np.zeros(len(Y))
    for fault in Y: #enough to check if all equals?++
        i=i+1
        if news[i]==0:
            for check in range(i+1,len(Y)):
                if np.array_equal(fault,Y[check]):
                    news[i]=1
                    news[check]=1
    
    detectable=3*(len(news)-np.count_nonzero(news))
    score=reward+detectable*app
    return score

def is_undetected(Y):
    i=-1
    news=np.zeros(len(Y))
    for fault in Y: #enough to check if all equals?++
        i=i+1
        if news[i]==0:
            for check in range(i+1,len(Y)):
                if np.array_equal(fault,Y[check]):
                    news[i]=1
                    news[check]=1
    
    return (np.count_nonzero(news)!=0)
    
def find_set(fault_activations,fault_manager,combos):
    no_isolable=[]
    base_set=[]
    
    
    #get those faults that cant be detectable and isolable so that are not taken into acount in the evaluation of the minimal sets
    i=-1
    for n in range(len(fault_activations)):
        go=True
        for j in no_isolable:
            if n in j:
                go = False
        # the group of no isolable faults are grouped     
        if go:
            new_fa=True
            if fault_activations[n]==[]:
                i=i+1
                no_isolable.append([n])
            else:
                if n<(len(fault_activations)-1):
                    for k in range(n+1,len(fault_activations)):
                        if compare_activation(fault_activations[n],fault_activations[k]):
                            if new_fa:
                                i=i+1
                                new_fa=False
                                no_isolable.append([n,k])
                            if k not in no_isolable[i]:
                                no_isolable[i].append(k)
                
    for no_go_set in no_isolable:
        for no_go in no_go_set:
            for mso in fault_activations[no_go]:
                if mso not in base_set:
                    base_set.append(mso)
        #fault_activations[no_go]=[-1]
        
    
    #with the undetected vector the faults that are left to be detected are highlighted       
    undetected=np.zeros(len(fault_activations)) # array to identify if the 
    team=0
    #to remove the non isolable or detectable faults from the iterative consideration
    fault_size=len(faults)
    excluded_faults=[]
    for no_go_set in no_isolable:
        if len(no_go_set)>1:
            team=team+1
            for no_go in no_go_set:
                fault_size=fault_size-1
                excluded_faults.append(no_go)
                undetected[no_go]=team
        else:
            fault_size=fault_size-1
            excluded_faults.append(no_go_set[0])
            undetected[no_go_set[0]]=-2
    
    #obtain a evaluation of each mso, the fewer appearances the higher the isolability they provide
    #in the same loop the reference marking of faults and msos is obtained without considering the non isolable/detrectable
    R=np.zeros([fault_size,len(fault_manager.models)])
    X=np.zeros([fault_size,len(fault_manager.models)])
    appearances=np.zeros(len(fault_manager.models))
    n=-1
    m=-1
    for t in fault_activations:
        m=m+1
        if m not in excluded_faults:
            n=n+1
            for mso in t:
                R[n][(mso-1)]=1
                appearances[(mso-1)]=appearances[(mso-1)]+1
            
    
    new_marking=np.zeros(fault_size)
    #the mso_set will include each step of the while loop, with a initial base_set for the msos required for the non isolable ones
    mso_set=[] # This is a PROBLEM !! The base set is too large and we dont avoid the msos already included to be considered again
    undetected=True
    
    while undetected:
        best=0
        for n in range(len(fault_manager.models)):
            if (n not in mso_set) and (appearances[n]>0):
                Y=copy.deepcopy(X)
                for m in range(fault_size):
                    if R[m][n]==1:
                        Y[m][n]=1
                test_set=copy.deepcopy(mso_set)
                test_set.append(n)
                if best<get_score(Y,appearances[n],fault_manager,test_set):
                    best=get_score(Y,appearances[n],fault_manager,test_set)
                    next_mso=n  # REMEMBER: The MSO were listed from 1 to N, but for the index in python it was changed to 0 to N-1 in this function
                    next_X=copy.deepcopy(Y)

        X=next_X
        mso_set.append(next_mso)
        undetected=is_undetected(X)
        # ALMOST WORKING !!!! Good score rule?
        # REMEMBER: The result require to include the MSOs that help to identify the non isolable sets removed before
       
    return mso_set,X  
    
############# RUN test for marking #############################
fault_manager.fault_signature_matrix()
result,X=find_set(fault_activations,fault_manager,combos)

################################################################
# Check that the solution doesn't have extra MSOs
def evaluate_result(result,X):
    evaluation=[]
    for n in result:
        test=np.delete(X,(n),1)
        neccesary=False
        i=0
        for fault in test:
            i=i+1
            for check in range(i,len(test)):
                if  np.array_equal(fault,test[check]):
                    neccesary=True
            if np.count_nonzero(fault)==0:
                neccesary=True
        
        if not neccesary:
            evaluation.append(n)
                    
    return evaluation
                    
evaluation=evaluate_result(result,X)
#lets do a second round of this
new_evaluation=[]
for reduce in evaluation:
    new_x=np.delete(X,(reduce),1)
    new_result=copy.deepcopy(result)
    new_result.remove(reduce)
    #fix indices
    for n in range(len(new_result)):
        if new_result[n]>reduce:
            new_result[n]=new_result[n]-1
    
    # remember that the new 
    new_evaluation.append([[reduce],[evaluate_result(new_result,new_x)]])

    
        
                

            