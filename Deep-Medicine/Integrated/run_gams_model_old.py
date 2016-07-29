#---------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#  ModuleName : run_gams_model
#  Function   : run_gams_model_single_run
#               run_gams_model
#
#  Input      : proc_data   - dataframe
#               featurelist - dataframe
#
#
#  Output :  list
#            run_gams_model_singlerun(model,predictedvalues,status)
#            run_gams_model(model,test_result,train_result,predicted_values, status="pass")
#
#            model             - robject
#            test_result       - list
#            train_result      - list
#            predicted_values  - dataframe
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Imports

import numpy as np
import rpy2
import pandas as pd
import pandas.rpy.common as com
import random
import math
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import IntVector, Formula
#rpy2.robjects.numpy2ri.activate()
mgcv = importr('mgcv')
base = importr('base')
statsf = importr('stats',robject_translations = {'format_perc': 'format_dot_perc'})


#Functions

def run_gams_model_single_run(proc_data,feature_list):

    if proc_data['outcome'] is not None:
           print("outcome variable found")
    else:
        print("outcome variable missing")
        return (list(None, None, status = "FAIL"))



    #Prepare Formula from feature list
    
    s="outcome~"
    for i in range(len(feature_list)):
        if(i in [37,49,48,51,72,50]):
            continue;
        if(feature_list['feature_type'][i] == 'num'):
            s += feature_list['feature_name'][i] + '+'
        else:
            s += feature_list['feature_name'][i] + '+'
    s = s[:-1]
    fmla = Formula(s)
    print s

    proc_data.dropna()
    response = proc_data['outcome']
    positiveOutcomes= np.sum(np.asarray(response))
    full_range = range(0, len(proc_data.index) - 1)
    thres_tune=round((positiveOutcomes/len(proc_data.index)),3)
    train_ind =random.sample(range(0,len(proc_data.index)-1),int(math.floor(0.7*len(proc_data.index))))
    test_ind = [val for val in full_range if val not in train_ind]
    rdf = com.convert_to_r_dataframe(proc_data.iloc[train_ind])
    #Run the model

    print("Running GAMs model")
    model = mgcv.bam(formula=fmla, data=rdf, family=statsf.binomial(link="logit"))
    print("Model building completed")

    #Predict the values

    tdf = com.convert_to_r_dataframe(proc_data)
    predval = statsf.predict(model, tdf, type="response")
    predicted_values = pd.concat([pd.DataFrame({'pred':predval}, index=[response.index.get_values()]), response], axis=1)
    predicted_values.columns = ['prediction', 'observed']

   #Returning the List
    status = "pass"
    res = list()
    res.append(model)
    res.append(predicted_values)
    res.append(status)
    print("+++++++++++++++++  Completed +++++++++++++++++++")
    return res


def run_gams_model(proc_data,feature_list):

    if proc_data['outcome'] is not None:
        print("outcome variable found")
    else:
        print("outcome variable missing")
        return (list(None,None,None,None,status = "FAIL"))


    # Prepare Formula from feature list

    s = "outcome~"
    for i in range(len(feature_list)):
        if(feature_list['feature_type'][i] == 'num'):
            s += feature_list['feature_name'][i] + '+'
        else:
            s += feature_list['feature_name'][i] + '+'

    s = s[:-1]
    fmla = Formula(s)

    # Create Sample dataFrame

    proc_data.dropna()
    response = proc_data['outcome']
    positiveOutcomes= np.sum(np.asarray(response))
    full_range = range(0, len(proc_data.index) - 1)
    test_result= list()
    train_result=list()
    thres_tune=round((positiveOutcomes/len(proc_data.index)),3)

    #Running Iterations

    print("Running GAMs iterations to report training and test performance")

    for i in range(1,50):
        print i
        train_ind = random.sample(range(0, len(proc_data.index) - 1), int(math.floor(0.7 * len(proc_data.index))))
        test_ind = [val for val in full_range if val not in train_ind]
        rdf = com.convert_to_r_dataframe(proc_data.iloc[train_ind])
        model = mgcv.bam(formula=fmla, data=rdf, family=statsf.binomial(link="logit"))
        #not sure how ashkans function is gonna return result
        #temp = perf_gam(model,proc_data.iloc[train_ind],proc_data.iloc[test_ind],thres_tune)
        #train_result.append(temp[0])
        #test_result.append(temp[1])

    tdf = com.convert_to_r_dataframe(proc_data)
    model = mgcv.bam(formula=fmla, data=tdf, family=statsf.binomial(link="logit"))
    print("Model building completed")

    #Predicting

    predval = statsf.predict(model, tdf, type="response")
    predicted_values = pd.concat([pd.DataFrame({'pred': predval}, index=[response.index.get_values()]), response],axis=1)
    predicted_values.columns = ['prediction', 'observed']

    print("+++++++++++++++++  Completed +++++++++++++++++++")

    # Returning the List
    status = "pass"
    res = list()
    res.append(model)
    res.append(test_result)
    res.append(train_result)
    res.append(predicted_values)
    res.append(status)

    return res




