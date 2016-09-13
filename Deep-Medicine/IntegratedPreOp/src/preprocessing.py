#pre-processing functions



import numpy as np
import pandas as pd
import re
import os
import re
from scipy.cluster.vq import kmeans, whiten, vq
from math import log
from re import sub
import rpy2
import pandas as pd
import pandas.rpy.common as com
import random
import math
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import IntVector, Formula
VIF_Lib = importr('VIF')

#---------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#  Function   :      outlier_detect
#                    median_deviation
# 
#  Importance  :     Removes the outliers by checking its z values
#
# 
#  Input      : vect   - dataframe
#               
#  Output     : new_vect- array
#               out_ind - array 
#-------------------------------------------------------------------------------------------------------

#calculates median deviation of an array
def median_deviation(vect):
    vect=pd.DataFrame(vect)
    vect = vect.astype(float)
    vect = vect[~pd.isnull(vect)]  
    vect = np.ma.array(vect).compressed() # should be faster to not use masked arrays.
    med = np.median(vect)
    return np.median(np.abs(vect - med))


#finds out the indexes of outlier samples	
def outlier_detect(vect):
    median_dev=median_deviation(vect)
    x_bar=np.nanmean(np.array(vect))
    vect=np.array(vect)
    vect_array=pd.DataFrame(vect)
    vect_array = vect_array[~pd.isnull(vect_array)]
    #find values corresponding to 0.01 quantile and 0.99 quantile
    minval=vect_array.quantile(q=0.01,axis=0)
    maxval=vect_array.quantile(q=0.99,axis=0)
    #find indexes having values less than 0.01 quantile and greater than 0.99 quantile values.
    ind_l=vect_array[vect_array[0]<minval[0]].index.tolist()
    ind_u=vect_array[vect_array[0]>maxval[0]].index.tolist()
    ind=vect_array[np.isnan(vect)].index.tolist()
    out_ind=[]
    if(len(ind)>0):
        #replaces na values with mean value of the column 
        vect_array.ix[ind]=x_bar
    #calculates z score for each value of the column 
    zvalue=pd.DataFrame(abs(0.6745*(vect-x_bar)))
    zvalue=(zvalue/median_dev)
    #checks high probability by checking z score
    ind1=(zvalue[zvalue[0]>5]).index.tolist()
    ind=np.intersect1d(ind1,ind_l,assume_unique=True)
    new_vect=vect_array
    if(len(ind)>0):
        new_vect.ix[ind]=np.reshape(np.random.uniform(vect_array.quantile(q=0.005,axis=0),vect_array.quantile(q=0.05,axis=0),len(ind)),(-1,1))
        # assign values between 0.005 quantile and 0.05 quantile of vect_array to new_vect for 
        # indexes having values less than 0.01 quantile and Z_score>5
        out_ind=ind
    ind=np.intersect1d(ind1,ind_u,assume_unique=True)
    if(len(ind)>0):
        new_vect.ix[ind]=np.reshape(np.random.uniform(vect_array.quantile(q=0.95,axis=0),vect_array.quantile(q=0.995,axis=0),len(ind)),(-1,1))
        # assign values between 0.95 quantile and 0.995 quantile of vect_array to new_vect for 
        # indexes having values greater than 0.99 quantile and Z_score>5
        out_ind=np.concatenate((out_ind,ind),axis=0)
    return new_vect,out_ind


#---------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#  Function   :      grouping_algo
# 
#  Importance  :     updating individual values of a column to 'OTHERS' whose count is less than 
#                    the threshold value(50)
#
#
#  Input      : vect_values   - dataframe
#               
#  Output     : vect - dataframe (Modified)
#-------------------------------------------------------------------------------------------------------

#type of vect will be tupple consisting of all column values and unique values of column
def grouping_algo(vect_values):
    vect=np.array(vect_values)
    thres=50
    vect_series = pd.Series(vect)
    #stroing count of each unique values from vect_Series
    vect_elem_count = vect_series.value_counts()
    ind=vect_elem_count[vect_elem_count<thres].index.tolist()
    if(len(ind)>0):
        low_prop=ind
        low_prop_set=set(low_prop)
        ind=[i for i, item in enumerate(vect) if item in low_prop_set]
        vect[ind]="OTHERS"
        vect_series = pd.Series(vect)
        vect_elem_count = vect_series.value_counts()
        ind=vect_elem_count[vect_elem_count>0].index.tolist()
        levels=ind
        #checking if count of 'OTHERS' values is less than threshold or not
        if(vect_elem_count['OTHERS']<thres):
            # check if total unique values is 2
            if(len(vect_elem_count.unique())==2):
                return vect
            vect_elem_count=pd.Series(vect_elem_count.sort_values())
            rep_level=vect_elem_count.index.tolist()
            vect[vect==rep_level[1]]="OTHERS"
    return vect
        

#---------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#  Function   :      clean_categorical
# 
#  Importance  :     preprocess the columns by substituting the missing_values like
#                    ["","MISSING","NA","UNKNOWN","_"," ",np.nan] to 'MISSING'
#                    Also update the column values with 'OTHERS' in case the count is
#                    less than the Threshold value
#
#  Calling Functions :  grouping_algo
#
#  Input      : vect   - dataframe
#               
#  Output     : vect - Series (Modified)
#-------------------------------------------------------------------------------------------------------
def clean_categorical(vect):
    vect_series=vect.ix[:,0]
    missing_values=["","MISSING","NA","UNKNOWN","_"," ",np.nan]
    ind=vect_series[vect_series.isin(missing_values)].index.tolist()
    if(len(ind)>0):
        #replacing missing values with  string 'Missing'
        vect_series[ind]="MISSING"
    vect=grouping_algo(vect_series)
    return vect   

def clean_categorical_VIF(vect):
    vect_series=vect.ix[:,0]
    missing_values=["","MISSING","NA","UNKNOWN","_"," ",np.nan]
    ind=vect_series[vect_series.isin(missing_values)].index.tolist()
    if(len(ind)>0):
        #replacing missing values with  string 'Missing'
        vect_series[ind]="MISSING"
    vect=grouping_algo(vect_series.astype(str))
    return vect 


"""
Substitutes values of the nominal variables (such as surgeon's ID) and categorical variables with more than two levels
with the corresponding log ratios

input : feature_input, outcome - Series Objects
        limit - int (minimum number of records for a categorical feature level in order not to be labeled as "other"
                     level)
        number_of_clusters - int (number of clusters in the "other" level in order to run a k-means algorithm and
                                  create number_of_clusters "new" levels instead of "other" level)

returns : output - dictionary with the following fields
                : d - ndarray (enumerated new levels of each input data record in feature_input)
                : vocabulary - ndarray (original levels)
                : cl_vocabulary (optional) - Pandas DataFrame (correspondence between the original "other" levels and
                                             the "new" ones (clusters))
                : p - ndarray (new levels)
                : cl_p (optional) - ndarray ("new" levels in the "other" level)

"""


def train_categorical_feature(feature_input, outcome, limit, number_of_clusters):
    
    input = feature_input.values
    
    if len(pd.unique(input)) == 2:
        vocabulary = np.unique(input)
        p = np.array([0, 1])
        d = np.zeros(len(input), dtype = np.int)
        d[input == vocabulary[1]] = 1
        output = dict(zip(["d", "vocabulary", "p"], [d, vocabulary, p]))
        print output
        return output
    
    vocabulary_t = pd.unique(input)
    count_1 = np.zeros(len(vocabulary_t), dtype = int)
    count_0 = np.copy(count_1)
    
    
    outcome_1 = outcome.values == 1
    outcome_0 = outcome.values == 0
    for index, item in enumerate(vocabulary_t):
        if pd.notnull(item):
            count_1[index] = sum((input == item) * (outcome_1))
            count_0[index] = sum((input == item) * (outcome_0))
        else:
            count_1[index] = sum(pd.isnull(input) * (outcome_1))
            count_0[index] = sum(pd.isnull(input) * (outcome_0))
    
    condition = (count_0 + count_1) >= limit
    condition[pd.isnull(vocabulary_t)] = True
#    n = sum(condition)
#    vocabulary = np.zeros(n, dtype = str)
#    p = np.zeros(n)
    
    def log_ratio(count_1, count_0):
        if count_1 == 0:
            return log(1/(2*float(count_0)))
        elif count_0 == 0:
            return log(2*count_1)
        else:
            return log(count_1/float(count_0))
        
    v_log_ratio = np.vectorize(log_ratio)
    
    vocabulary = vocabulary_t[condition]
    p = v_log_ratio(count_1[condition], count_0[condition])
    
#    index = 0
#    for i in range(len(vocabulary_t)):
#        if (condition[i]):
#            vocabulary[index] = str(vocabulary_t[index])
#            p[index] = log_ratio(count_1[index], count_0[index])
#            index = index + 1
#            if (count_1[index] == 0):
#                p[index] = log(1./(2*count_0[index]))
#            elif (count_0[index] == 0):
#                p[index] = log(2*count_1[index])
#            else:
#                p[index] = log(count_1[index]./count_0[index])
    # print "sum(condition == 0) is {0}".format(sum(condition == 0))
    if sum(condition == 0) <= 1:
        if sum(condition == 0) == 1:
            p = np.append(p, log_ratio(count_1[condition == 0][0], count_0[condition == 0][0]))
#           if (count_1[condition == 0][0] == 0):
#                p[condition == 0] = log(1./(2*count_0[condition == 0][0]))
#           elif (count_0[condition == 0] == 0):
#                p[condition == 0] = log(2*count_1[condition == 0][0])
#           else:
#                p[condition == 0] = log(count_1[condition == 0][0]./count_0[condtion == 0][0])
            vocabulary = np.append(vocabulary, vocabulary_t[condition == 0])
    else:
        # print "number of clusters {0}".format(number_of_clusters)
        cl = min(number_of_clusters, sum(condition == 0) - 1) # why is it -1 here?
        # cl_vocabulary = pd.DataFrame()
        # print "cl {0}".format(cl)
        residual_1 = count_1[condition == 0]
        residual_0 = count_0[condition == 0]
        # print "length of the residual_1 {0}".format(len(residual_1))
#        s = np.zeros(len(residual_1))
        s = v_log_ratio(residual_1, residual_0).reshape([len(residual_1), 1]) 
        whitened = whiten(s)
        codebook = kmeans(whitened, cl)[0]
        code = vq(whitened, codebook)[0]
        # print "length of code {0}".format(len(code))
        s1 = pd.Series(data = vocabulary_t[condition == 0]) # .astype(str)
        s2 = pd.Series(data = code)
        cl_vocabulary = pd.DataFrame.from_dict({"cat_feature_input": s1, "cluster_id": s2})

        #print cl_vocabulary.axes

        cl_p = np.zeros(cl, dtype = float)
        # print cl_p, len(cl_p)
        
        for i in range(cl):
            # print i
            c1 = residual_1[code == i]
            c0 = residual_0[code == i]
            cl_p[i] = log_ratio(sum(c1), sum(c0))
            # print "Hey"
    
    d = np.zeros(len(input))
    d[pd.isnull(input)] = p[pd.isnull(vocabulary)]
    
    for i in range(len(vocabulary)):
        d[input == vocabulary[i]] = p[i]
    vocabulary = vocabulary.astype(str)

    if 'cl_vocabulary' in locals():
        print "cl_vocabulary in locals()"
        for i in range(len(cl_vocabulary)):
            d[input == cl_vocabulary.loc[i, "cat_feature_input"]] = cl_p[cl_vocabulary.loc[i, "cluster_id"]]
        #print cl_vocabulary.axes
        cl_vocabulary.loc[:, "cat_feature_input"] = cl_vocabulary["cat_feature_input"].astype(str)
        # print cl_vocabulary["cat_feature_input"].apply(type)
    
        output = dict(zip(["d", "vocabulary", "cl_vocabulary", "p", "cl_p"], [d, vocabulary, cl_vocabulary, p, cl_p]))
    else:
        output = dict(zip(["d", "vocabulary", "p"], [d, vocabulary, p]))

    #print output
    return output

def train_procedure_feature(data, outcome, limit):
    lowlim = np.array([100, 101, 106, 108, 117, 118, 121, 130, 135, 140, 142, 155, 160, 165, 172, 176, 185, 187])
    procedures = np.zeros_like(data,dtype=float)
    groups =(np.zeros((20000,2)))
    
    for i in xrange(len(data)):
        if(pd.isnull(data[i])):
            data[i]=0
        if(data[i]==0):
            s="00"
        else:
            s = str(data[i])  
        for k in xrange(len(s),1,-1):  
            j = int("1"+s[0:k])
            if(outcome[i] == 1):
                    groups[j,0]= groups[j,0]+1  
            else:
                groups[j,1]= groups[j,1]+1
   
        num = int("1"+s[0:2])
        for j in xrange((len(lowlim)),0,-1):
            if(num>=lowlim[j-1]):
                if outcome[i]==1:
                    groups[j,0]=groups[j,0]+1
                else:
                    groups[j,1]=groups[j,1]+1
                break;

    for i in range(1,(len(lowlim)+1),1):
        if(groups[i,0]+groups[i,1] < limit):
            groups[0,0]=groups[0,0]+groups[i,0]
            groups[0,1]=groups[0,1]+groups[i,1]
            groups[i,0]=0
            groups[i,1]=0

    for i in range(len(data)):
        flag = 0
        k=0
        s=str(data[i])
        while(k<=len(s)-2):
            ind = int("1"+s[0:len(s)-k])
            if(groups[ind,0]+groups[ind,1]>=limit):
                if(groups[ind,0]==0):
                    procedures[i]=np.log(1/(2*groups[ind,1]))
                elif(groups[ind,1]==0):
                    procedures[i]=np.log(2*groups[ind,0])
                else:
                    procedures[i]=np.log(groups[ind,0]/groups[ind,1])
                flag = 1
                break
            k = k+1
        if(flag==0):
            q = int("1"+s[0:2])
            for j in xrange((len(lowlim)),2,-1):
                if(q>=lowlim[j-1]):
                    if(groups[j,0]+groups[j,1] > 0):
                        if(groups[j,0]==0):
                            procedures[i]=np.log(1/(2*groups[j,1]))
                        elif(groups[j,1]==0):
                            procedures[i]=np.log(2*groups[j,0])
                        else:
                            procedures[i]=np.log(groups[j,0]/groups[j,1])
                    else:
                        if(groups[0,0]==0):
                            procedures[i]=np.log(1/(2*groups[0,1]))
                        elif(groups[0,1]==0):
                            procedures[i]=np.log(2*groups[0,0])
                        else:
                            procedures[i]=np.log(groups[0,0]/groups[0,1])
                        break
    
    output = {"procedures":procedures, "groups":groups}
    return output


def get_procedure_feature(data, groups, limit):
    lowlim = np.array([100, 101, 106, 108, 117, 118, 121, 130, 135, 140, 142, 155, 160, 165, 172, 176, 185, 187])
    procedures = np.zeros_like(data,dtype=float)
    
    for i in range(len(data)):
        flag = 0
        k=0
        s=str(data[i])
        while(k<=len(s)-2):
            ind = int("1"+s[0:len(s)-k])
            if(groups[ind,0]+groups[ind,1]>=limit):
                if(groups[ind,0]==0):
                    procedures[i]=np.log(1/(2*groups[ind,1]))
                elif(groups[ind,1]==0):
                    procedures[i]=np.log(2*groups[ind,0])
                else:
                    procedures[i]=np.log(groups[ind,0]/groups[ind,1])
                flag = 1
                break
            k = k+1
        if(flag==0):
            q = float("1"+s[0:2])
            for j in xrange((len(lowlim)),2,-1):
                if(q>=lowlim[j-1]):
                    if(groups[j,0]+groups[j,1] > 0):
                        if(groups[j,0]==0):
                            procedures[i]=np.log(1/(2*groups[j,1]))
                        elif(groups[j,1]==0):
                            procedures[i]=np.log(2*groups[j,0])
                        else:
                            procedures[i]=np.log(groups[j,0]/groups[j,1])
                    else:
                        if(groups[0,0]==0):
                            procedures[i]=np.log(1/(2*groups[0,1]))
                        elif(groups[0,1]==0):
                            procedures[i]=np.log(2*groups[0,0])
                        else:
                            procedures[i]=np.log(groups[0,0]/groups[0,1])
                        break

    return procedures


#---------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#  ModuleName :      gen_proc_data
#  Function   :      gen_proc_data
# 
#  Importance  :      It is used to pre-process the data by removing the outliers and
#                     transforming categorical data
#
#  Calling Functions:   outlier_detect
#                       train_procedure_feature
#                       train_categorical_feature
#                       clean_categorical
#
#  Input      : raw_data   - dataframe (data read from excel file)
#               feature_list - dataframe (data from excel containing features name and its corresponding type)
#               outcome      - dataframe (actual outcome data)
#
#  Output :   raw_data - dataframe (after pre-processing)
#-------------------------------------------------------------------------------------------------------


def gen_proc_data(raw_data,feature_list,outcome):
    t=np.repeat(np.array([0]),len(outcome), axis=0)
    series=pd.Series(t)
    series[outcome==1]=1
    pd.options.mode.chained_assignment = None
    #storing columns names and its type in two separate list
    feature_new_list = list(feature_list.ix[:,0])
    feature_list_type= list(feature_list.ix[:,1])
    #removes values from 'Admission_Source' equal to 'NaN','' to default value 'outpatient'
    raw_data['Admission_Source'].fillna('',inplace=True)
    raw_data['Admission_Source'] = raw_data['Admission_Source'].apply(lambda x: 'outpatient' if x=="" else x)
    #gets the intersection of columns common to both raw_data and feature_list
    raw_data=raw_data[list(set(feature_new_list) & set(list(raw_data.columns.values)))]
    raw_data['outcome']=pd.DataFrame(series)
    #sets all Outcome values to either 0 or 1
    if(len(set(list(raw_data.columns.values)))!=len(feature_new_list)):
        print("fields mismatch in feature list and raw data, following not found in raw data")
        print(list(set(feature_new_list).difference(set(list(raw_data.columns.values)))))
    for i in range(0,len(feature_new_list)):
        ind=[j for j in raw_data.columns.values if j in feature_new_list[i]]
        if(len(ind)==0):
            print (feature_new_list[i])   
            continue
        if(len(ind)>1):
            ind=ind[0]
        if(feature_list_type[i]=="num"):
            #removes Outliers from the column having numeric data
            new_data,outlier_index=outlier_detect(raw_data[ind])
            new_data.columns = ind
            raw_data[ind]=new_data
            continue
        if((feature_list_type[i]=="cat")and(feature_new_list[i]=="pr1c")):
            t=raw_data['pr1c'].apply(lambda s: re.subn(r'[^0-9]', "", s)[0])
            d=train_procedure_feature(t,outcome,100)
            raw_data[ind]=d['procedures']
            continue
        if(feature_list_type[i]=="cat"and(len(np.unique(raw_data[ind]))>5)):
            d=train_categorical_feature(raw_data[ind[0]],outcome,1,2)
            #check TrainCategoricalFeature function for details
            raw_data[ind]=d['d']
            continue
        else:
            raw_data[ind]=clean_categorical(raw_data[ind])
    return raw_data


def function vif_test(raw_data, outcome, feature_list):

    t=np.repeat(np.array([0]),len(outcome), axis=0)
    series=pd.Series(t)
    series[outcome==1]=1
    raw_data["Admission_Source"].fillna(value = "outpatient", inplace = True)

    raw_data = raw_data[list(set(feature_list["feature_name"].values) & set(raw_data.columns))]
    raw_data['outcome']=pd.DataFrame(series)
    if (len(raw_data.columns) != len(feature_list)):
        print "fields mismatch in feature list and raw data, following features are not found in raw data"
        print (set(feature_list["feature_name"].values) - set(raw_data.columns))
        print "execution terminated"
        return

    for i, item in enumerate(feature_list["feature_name"]):
        ind = raw_data.columns.values[raw_data.columns == item]
        #print i, item, type(item), ind
        if len(ind) == 0:
            print item
            continue
        if len(ind) > 1:
            ind = [ind[0]]
        # print i, item, feature_list["feature_type"].iloc[i]
        if feature_list["feature_type"].iloc[i] == "num":
            new_data,outlier_index=outlier_detect(raw_data[ind])
            new_data.columns = ind
            raw_data[ind]=new_data
            continue
        if feature_list["feature_type"].iloc[i] == "cat" and item == "pr1c":
            t=raw_data['pr1c'].apply(lambda s: re.subn(r'[^0-9]', "", s)[0])
            d=train_procedure_feature(t,outcome,100)
            raw_data[ind]=d['procedures']
            continue
        else:
            d=train_categorical_feature(raw_data[ind[0]],outcome,1,2)
            #check TrainCategoricalFeature function for details
            raw_data[ind]=d['d']

    x = raw_data
    y = outcome

    # R code

    #t <- vif(y,x,mode="dense",trace = F,subsize = round(0.6*length(y),0))
    #selected_features <- feature_list[t$select,]
    #return(selected_features)