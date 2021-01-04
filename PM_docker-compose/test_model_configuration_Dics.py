# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:54:49 2020

@author: sega01
"""

# LIST of model constructions for the A-H testing: 60000 train samples, 10000 test and 10000 kde
# "_testB_201204"
{"layers":[{"Layer":"LR","k":10,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":8},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":6},
           {"Layer":"L","k":4},
           {"Layer":"L","k":3}],
 "adam":0.002
}

# "_testC_201204"
{"layers":[{"Layer":"LR","k":10,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":8,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":6,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":4,"l2":0.001},
           {"Layer":"D","d":0.05},
           {"Layer":"LR","k":3,"l2":0.001}],
 "adam":0.002
}


# "_testD_201204"
{"layers":[{"Layer":"L","k":8},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":6},
           {"Layer":"L","k":4},
           {"Layer":"L","k":2}],
 "adam":0.002
}          
           
# "_testE_201204"
{"layers":[{"Layer":"LR","k":8,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":6},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":4},
           {"Layer":"L","k":2}],
 "adam":0.002
}        

# "_testF_201204"
{"layers":[{"Layer":"LR","k":8,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":6,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":4,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":2,"l2":0.001}],
 "adam":0.002
}       

 
# "_testG_201204"  
{"layers":[{"Layer":"LR","k":5,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":4,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":3,"l2":0.001},
           {"Layer":"D","d":0.1}],
 "adam":0.002
}           
        

# "_testH_201204"  
{"layers":[{"Layer":"LR","k":5},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":4},
           {"Layer":"L","k":3}],
 "adam":0.002
}

# "_testA_201204"  == "_test_versions_201202"
{"layers":[{"Layer":"LR","k":5,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":4},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":3}],
 "adam":0.002
}


# LIST of model constructions for the second round of testing: 90000 train samples, 15000 test and 15000 kde

# "_test_2A_201211"  == "_testA_201204"
{"layers":[{"Layer":"LR","k":5,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":4},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":3}],
 "adam":0.002
}

# "_test_2B_201211" == "_testB_201204"
{"layers":[{"Layer":"LR","k":10,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":8},
           {"Layer":"D","d":0.1},
           {"Layer":"L","k":6},
           {"Layer":"L","k":4},
           {"Layer":"L","k":3}],
 "adam":0.002
}

# "_test_2C_201211"== "_testC_201204"
{"layers":[{"Layer":"LR","k":10,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":8,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":6,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":4,"l2":0.001},
           {"Layer":"D","d":0.05},
           {"Layer":"LR","k":3,"l2":0.001}],
 "adam":0.002
}

# "_test_2D_201211"
{"layers":[{"Layer":"LR","k":10,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":8,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":6,"l2":0.001},
           {"Layer":"D","d":0.05},
           {"Layer":"L","k":4},
           {"Layer":"D","d":0.05},
           {"Layer":"L","k":3}],
 "adam":0.002
}

# "_test_2E_201211"
{"layers":[{"Layer":"LR","k":15,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":12,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":8,"l2":0.001},
           {"Layer":"D","d":0.05},
           {"Layer":"LR","k":6,"l2":0.001},
           {"Layer":"D","d":0.05},
           {"Layer":"LR","k":3,"l2":0.001}],
 "adam":0.002
}

# "_test_2F_201211"
{"layers":[{"Layer":"LR","k":10,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":8,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":8,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":6,"l2":0.001},
           {"Layer":"D","d":0.05},
           {"Layer":"LR","k":6,"l2":0.001},
           {"Layer":"D","d":0.05},
           {"Layer":"LR","k":4,"l2":0.001},
           {"Layer":"LR","k":4,"l2":0.001},
           {"Layer":"LR","k":2,"l2":0.001}],
 "adam":0.002
}

# "_test_3A_201222"
{"layers":[{"Layer":"LR","k":15,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":10,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":10,"l2":0.001},
           {"Layer":"D","d":0.1},
           {"Layer":"LR","k":8,"l2":0.001},
           {"Layer":"D","d":0.05},
           {"Layer":"LR","k":6,"l2":0.001},
           {"Layer":"D","d":0.05},
           {"Layer":"LR","k":4,"l2":0.001},
           {"Layer":"LR","k":4,"l2":0.001},
           {"Layer":"LR","k":2,"l2":0.001}],
 "adam":0.002
}


for mso in fm.mso_set:   
    name=folder+'MSO_Model_'+str(mso) #str(self.mso_index)
    name_att=name+'.pkl'
    filehandler = open(name_att, 'rb') 
    variables = pickle.load(filehandler)
    filehandler.close()
    for att in variables:
        setattr(fm.models[mso],att,variables[att])
    fm.models[mso].spec_list=list_o
    variables=fm.models[mso].__dict__
    file = open(name_att, 'wb')
    pickle.dump(variables, file)
    file.close()
#self.build_model_nn(self.shape_nn,len(self.source))
#self.model.load_weights(name)