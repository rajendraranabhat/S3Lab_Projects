
from read_data import read_data
from outlier_detect import outlier_detect
from train_procedure_feature import train_procedure_feature
from clean_categorical import clean_categorical
import numpy as np
import pandas as pd
from re import sub
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.com as com

"""
Performs vif (variance inflation factor) test

input : raw_data, feature_list - Pandas DataFrames
        outcome - Series Object

returns : selected_features - ?

"""

def vif_test(raw_data, outcome, feature_list):

    temp = np.zeros(len(outcome))
    temp[outcome.values == 1] = 1
    outcome = temp

    raw_data["Admission_Source"].fillna(value = "outpatient", inplace = True)

    raw_data = raw_data[list(set(feature_list["feature_name"].values) & set(raw_data.columns))]

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
            temp = outlier_detect(raw_data[item])
            raw_data[item] = temp[0]
            continue
        if feature_list["feature_type"].iloc[i] == "cat" and item == "pr1c":
            temp = raw_data[item]
            temp = temp.apply(lambda x: sub(r"[^0-9]", "", x))
            d = train_procedure_feature(temp, outcome, 100)
            raw_data[item] = pd.Series.from_array(d["procedures"])
            # print raw_data[item]
            continue
        else:
            temp = clean_categorical(raw_data[item])
            d = train_categorical_feature(temp, outcome, 100, 2)
            raw_data[item] = pd.Series.from_array(d["d"])

    x = raw_data
    y = outcome

    # R code

    # t <- vif(y,x,mode="dense",trace = F,subsize = round(0.6*length(y),0))
    # selected_features <- feature_list[t$select,]
    # return(selected_features)


