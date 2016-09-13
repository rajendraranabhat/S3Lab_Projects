from read_data import *
from preprocessing import *
from run_gams_model import *
import numpy as np
import pandas as pd

data_raw,features,features_all=read_data()
features_selected=features_all.drop(features_all.index[[37,50,51,72,73]])

# run for CV complication
proc_data=gen_proc_data(data_raw,features_selected,data_raw['cv_comp_new'])
models_cvcomp=get_all_gams_model(proc_data,features_selected)
best_model_cvcomp=get_best_model(models_cvcomp)
r_df_cvcomp = com.convert_to_r_dataframe(proc_data)
pred_score_cvcomp= statsf.predict(best_model_cvcomp,r_df_cvcomp, type="response")
pred_obser_cvcomp=proc_data['outcome'];
best_model_metric=calculate_metric(pred_obser_cvcomp,pred_score_cvcomp)
cutoff1_cvcomp=best_model_metric['thres'].iloc[best_model_metric['yod_index'].idxmax()-1]
cutoff2_cvcomp=cal_cutoff2(best_model_metric)
predicted_values_cvcomp =pd.DataFrame({'prediction':pred_score_cvcomp}, index=range(0,len(pred_score_cvcomp)))
predicted_values_cvcomp.ix[predicted_values_cvcomp.prediction <= cutoff1_cvcomp 'category'] = 'low'
predicted_values_cvcomp.ix[predicted_values_cvcomp.prediction >cutoff2_cvcomp, 'category'] = 'high'
predicted_values_cvcomp.ix[(predicted_values_cvcomp.prediction <=cutoff2_cvcomp) & (predicted_values_cvcomp.prediction>cutoff1_cvcomp), 'category'] = 'moderate'


# run for MV complication

proc_data=gen_proc_data(data_raw,features_selected,data_raw['MV_comp'])
models_mvcomp=get_all_gams_model(proc_data,features_selected)
best_model_mvcomp=get_best_model(models_mvcomp)
r_df_mvcomp = com.convert_to_r_dataframe(proc_data)
pred_score_mvcomp= statsf.predict(best_model_mvcomp,r_df_mvcomp, type="response")
pred_obser_mvcomp=proc_data['outcome'];
best_model_metric=calculate_metric(pred_obser_mvcomp,pred_score_mvcomp)
cutoff1_mvcomp=best_model_metric['thres'].iloc[best_model_metric['yod_index'].idxmax()-1]
cutoff2_mvcomp=cal_cutoff2(best_model_metric)
predicted_values_mvcomp =pd.DataFrame({'prediction':pred_score_mvcomp}, index=range(0,len(pred_score_mvcomp)))
predicted_values_mvcomp.ix[predicted_values_mvcomp.prediction <= cutoff1_mvcomp, 'category'] = 'low'
predicted_values_mvcomp.ix[predicted_values_mvcomp.prediction >cutoff2_mvcomp, 'category'] = 'high'
predicted_values_mvcomp.ix[(predicted_values_mvcomp.prediction <=cutoff2_mvcomp) & (predicted_values_mvcomp.prediction>cutoff1_mvcomp), 'category'] = 'moderate'

# run for icu complicaton
proc_data=gen_proc_data(data_raw,features_selected,data_raw['ICU_comp'])
models_icucomp=get_all_gams_model(proc_data,features_selected)
best_model_icucomp=get_best_model(models_icucomp)
r_df_icucomp = com.convert_to_r_dataframe(proc_data)
pred_score_icucomp= statsf.predict(best_model_icucomp,r_df_icucomp, type="response")
pred_obser_icucomp=proc_data['outcome'];
best_model_metric=calculate_metric(pred_obser_icucomp,pred_score_icucomp)
cutoff1_icucomp=best_model_metric['thres'].iloc[best_model_metric['yod_index'].idxmax()-1]
cutoff2_icucomp=cal_cutoff2(best_model_metric)
predicted_values_icucomp =pd.DataFrame({'prediction':pred_score_icucomp}, index=range(0,len(pred_score_icucomp)))
predicted_values_icucomp.ix[predicted_values_icucomp.prediction <= cutoff1_icucomp, 'category'] = 'low'
predicted_values_icucomp.ix[predicted_values_icucomp.prediction >cutoff2_icucomp, 'category'] = 'high'
predicted_values_icucomp.ix[(predicted_values_icucomp.prediction <=cutoff2_icucomp) & (predicted_values_icucomp.prediction>cutoff1_icucomp), 'category'] = 'moderate'

# run for 30 day mortality complicaton
proc_data_num=gen_proc_data(data_raw,features_selected,data_raw['mort_status_30d'])
models_30dmort=get_all_gams_model(proc_data,features_selected)
best_model_30dmort=get_best_model(models_30dmort)
r_df_30dmort = com.convert_to_r_dataframe(proc_data)
pred_score_30dmort= statsf.predict(best_model_30dmort,r_df_30dmort, type="response")
pred_obser_30dmort=proc_data['outcome'];
best_model_metric=calculate_metric(pred_obser_30dmort,pred_score_30dmort)
cutoff1_30dmort=best_model_metric['thres'].iloc[best_model_metric['yod_index'].idxmax()-1]
cutoff2_30dmort=cal_cutoff2(best_model_metric)
predicted_values_30dmort =pd.DataFrame({'prediction':pred_score_30dmort}, index=range(0,len(pred_score_30dmort)))
predicted_values_30dmort.ix[predicted_values_30dmort.prediction <= cutoff1_30dmort, 'category'] = 'low'
predicted_values_30dmort.ix[predicted_values_30dmort.prediction >cutoff2_30dmort, 'category'] = 'high'
predicted_values_30dmort.ix[(predicted_values_30dmort.prediction <=cutoff2_30dmort) & (predicted_values_30dmort.prediction>cutoff1_30dmort), 'category'] = 'moderate'
