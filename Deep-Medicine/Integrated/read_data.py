
import os
import pandas as pd
import numpy as np
import math
from re import sub

"""
Reads data and feature lists from csv files

returns : data_raw, features, features_all - Pandas DataFrames

NOTE: a path to the folder with the csv files should be entered manually!
"""

def read_data():
    # path = ''  #give path
    # data_raw = pd.read_csv(path+"data_11_26_2015_115vars.csv")
    # features = pd.read_csv(path+"feature_list.csv")
    # features_all = pd.read_csv(path+"feature_list_all.csv")
    path = './'  # give path
 #   data_raw = pd.read_csv(path + "Fake Data.csv", thousands = ',', converters = {"Med_inc": lambda x: int(x.translate(None, "$,"))})
    data_raw = pd.read_csv("/Volumes/FILES-1/ANES/SHARE/research/PRISMAP Studies/"
        "IDEALIST/4 IDEALIST Analytic Core/Prediction of PC/Preop Data for Analysis/"
        "data_11_26_2015_116vars_ordered_clean.csv", thousands = ','
                           #, converters = {"Med_inc": lambda x: x}\
        , converters = {"Med_inc": lambda x: float(x.translate(None, "$,")) if (x != '') else np.nan
            , "zip5": lambda x: sub(r"[.].*", "", x) if (x != '') else np.nan}
                           #, na_values = {"Med_inc": ""})
        )

    features = pd.read_csv(path + "feature_list.csv")
    features_all = pd.read_csv(path + "feature_list_all.csv")


    # Indicator of receiving nephrotoxic drug on admission day
    def nephtox_adm(x):
        if (x['nsaids_adm'] == 1 and (x['vanco_adm'] == 1 or x['diuret_adm'] ==1 or x['aminog_adm'] ==1)):
            t = 2
        elif(x['nsaids_adm'] == 1):
            t = 1
        else:
            t = 0
        return t
    
    data_raw['nephtox_adm'] = -1 
    # data_raw[['nsaids_adm', 'vanco_adm', 'diuret_adm', 'aminog_adm', 'nephtox_adm']]
    data_raw['nephtox_adm'] = data_raw.apply(nephtox_adm, axis = 1)
    # data_raw[['nsaids_adm', 'vanco_adm', 'diuret_adm', 'aminog_adm', 'nephtox_adm']]

    # data_all = pd.read_csv(path+"data_11_26_2015.csv")
    # data_all = pd.read_csv(path + "Fake Data.csv", thousands = ',', converters = {"Med_inc": lambda x: x[1:]})

    # data_raw['Admitting_type'] = data_all['Admitting_type']

    #create Number of nephrotoxic medications
    adm_lst = ["aminog_adm", "diuret_adm", "vanco_adm","ace_adm", "nsaids_adm", "inot_pres_adm"]
    index = [col for col in data_raw if col in adm_lst]
    data_raw['no_nephrotoxic_meds'] = data_raw[index].sum(axis = 1)

    # grouping Urine Protein
    def max_protur_gr2(x):
        if(x == '>=300'): 
            t = 2 
        elif(x == 'TR-30-100'): 
            t = 1 
        else: 
            t = 0
        return t
    data_raw['max_PROTUR_gr2'] = data_raw['max_PROTUR_gr2'].map(max_protur_gr2)

    #grouping Urinal hemoglobin
    def max_gr(x):
        if(x == 'Large'):
            t = 2
        elif(x == 'Missing' or x == 'NEGATIVE'):
            t = 0
        else:
            t = 1
        return t
    data_raw['max_HGBUR_gr'] = data_raw['max_HGBUR_gr'].map(max_gr)

    #grouping Urinal glucose
    data_raw['max_GLUURN_gr'] = data_raw['max_GLUURN_gr'].map(max_gr)

    # grouping of No of complete blood count tests
    def count_HGBn(x):
        if(x == 0):
            t = 0
        elif(x == 1):
            t = 1
        else:
            t = 2 #'2 or more'
        return t
    data_raw['count_HGBn'] = data_raw['count_HGBn'].map(count_HGBn)
    
    return data_raw, features, features_all

