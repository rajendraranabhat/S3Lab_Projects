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


import numpy as np
import rpy2
import pandas as pd
import pandas.rpy.common as com
import random
import math
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import IntVector, Formula
from sklearn.metrics import roc_auc_score
#rpy2.robjects.numpy2ri.activate()
mgcv = importr('mgcv')
base = importr('base')
statsf = importr('stats',robject_translations = {'format_perc': 'format_dot_perc'})


#Functions

def gams_for_individual_run(proc_data,feature_list):

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

    proc_data.dropna()
    full_range = range(0, len(proc_data.index) - 1)
    #thres_tune=round((positiveOutcomes/len(traindata.index)),3)
    train_ind =random.sample(range(0,len(proc_data.index)-1),int(math.floor(0.7*len(proc_data.index))))
    test_ind = [val for val in full_range if val not in train_ind]
    response = proc_data['outcome'].iloc[test_ind]
    rdf = com.convert_to_r_dataframe(proc_data.iloc[train_ind])
    #Run the model

    print("Running GAMs model")
    model = mgcv.bam(formula=fmla, data=rdf, family=statsf.binomial(link="logit"))
    print("Model building completed")

    #Predict the values

    tdf = com.convert_to_r_dataframe(proc_data.iloc[test_ind])
    predval = statsf.predict(model, tdf, type="response")
    predicted_values = pd.concat([pd.DataFrame({'pred':predval}, index=[response.index.get_values()]), response], axis=1)
    predicted_values.columns = ['prediction', 'observed']
    auc=roc_auc_score(response, predval)
    status = "pass"
    res = list()
    res.append(model)
    res.append(predicted_values)
    res.append(auc)
    print("+++++++++++++++++  Completed +++++++++++++++++++")
    return res

def get_all_gams_model(proc_data,feature_list):
    print("Running GAMs iterations to report training and test performance")
    res=list()
    for i in range(1,3):
        temp1_1=gams_for_individual_run(proc_data,features_selected)
        res.append(temp1_1)
    return res;

def cal_cutoff2(data):
    val=0
    for i in range(len(data)-10):
        if((abs(data['acc'].iloc[i]-data['acc'].iloc[i+10]))<0.002):
            val=data['thres'].iloc[i]
            break
    return(val)

def get_best_model(final):
    max_auc=final[0][2]
    best_model=final[0][0];
    for i in range(len(final)):
        if(max_auc<final[i][2]):
            max_auc=final[i][2];
            best_model=final[i][0];
    return best_model


def ROC_parameters(obser,score,thr):
    #print obser,score,thr
    temp=np.zeros(len(score))
    #print thr;
    temp[[ i for i, x in enumerate(score) if x >= thr ]]= 1
    p_ind=[ i for i, x in enumerate(obser) if x == 1 ]
    n_ind = [ i for i, x in enumerate(obser) if x == 0 ]
    TP = sum(temp[p_ind]==1)
    FP = sum(temp[n_ind]==1)
    TN =sum(temp[n_ind]==0)
    FN = sum(temp[p_ind]==0)
    acc = (float)(TP+TN)/len(temp)
    #print TP,FP,TN,FN;
    ppv = (float)(TP)/(TP+FP) ; 
    npv = (float)(TN)/(TN+FN)
    sen = (float)(TP)/(TP+FN) ; 
    spe = (float)(TN)/(TN+FP)
    yod = (float)(sen+spe-1)
    ls=list();
    ls.append(acc)
    ls.append(ppv)
    ls.append(npv)
    ls.append(sen)
    ls.append(spe)
    ls.append(yod)
    return ls

  
def calculate_metric(outcome, score):
    obser = np.zeros(len(outcome))
    obser[[i for i, x in enumerate(outcome) if x == 1 ]] = 1 ;
    obser = [float(i) for i in obser]
    score = [float(i) for i in score]
    prev = round(sum(obser)/len(obser),2)
    thres = np.arange(0.01,0.98,0.01)
    xval = thres
    acc = np.zeros(len(thres))
    ppv = np.zeros(len(thres))
    npv = np.zeros(len(thres))
    sen = np.zeros(len(thres))
    spe = np.zeros(len(thres))
    yod = np.zeros(len(thres))
    auc = np.zeros(len(thres))
    for l in range(len(thres)):
        plotdata = ROC_parameters(obser,score,thres[l])
        acc[l] = round(plotdata[0],3)
        ppv[l] = round(plotdata[1],3)
        npv[l] = round(plotdata[2],3)
        sen[l] = round(plotdata[3],3)
        spe[l] = round(plotdata[4],3)
        yod[l] = round(plotdata[5],3)
        auc[l] = roc_auc_score(obser, score)

    prev = round(sum(obser)/len(obser),2)
    #roc_vals=np.zeros((length(spe),8))
    roc_vals=pd.DataFrame(index=range(1,98), columns=[["thres","acc","ppv","npv","specificity","sensitivity","yod_index","auc"]])
    #roc_vals <- dacolnames(roc_vals) <- c("thres","acc","ppv","npv","specificity","sensitivity","yod_index","auc")
    roc_vals['thres']=thres
    roc_vals['acc']= acc
    roc_vals['ppv'] = ppv
    roc_vals['npv'] = npv
    roc_vals['specificity'] =spe
    roc_vals['sensitivity'] = sen
    roc_vals['yod_index'] = yod;
    roc_vals['auc'] = auc;
    return roc_vals
