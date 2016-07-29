# This the main file that reads the user defined functions and data required. 
# The functions file functions1.R and functions2.R are the user defined functions for data processing and model building
# functions_plot.R : functions for generating performance plot 

########
# This flow was created based on the initial 2 stage approach 
# step1. using gams model predict risk and categorize patients into low, medium and high risk categories
# step2. using svm model on the low and medium risk patients, reclassify them to low and high risk
########


# remove few features
features_selected <- features_all[-c(38,51,52,73,74),]

# run for CV complication
proc_data <- gen_proc_data(data_raw,features_selected,data_raw$cv_comp_new)
sel_list_vif <- vif_test(data_raw,outcome =data_raw$cv_comp_new,feature_list = features_selected )
temp1_1 <- run_gams_model_single_run(proc_data,sel_list_vif)

t <- temp1_1$predicted_values
predictions <- as.data.frame(cbind(data_raw$Account,temp1_1$predicted_values))
print(predictions)

t$category <- ifelse(t$predicted<=0.07,"low",ifelse(t$predicted>0.35,"high","moderate"))
temp1_1$predicted_values$category <- t$category 

# run for MV complication
proc_data <- gen_proc_data(data_raw,features_selected,data_raw$MV_comp)
sel_list_vif <- vif_test(data_raw,outcome =data_raw$MV_comp,feature_list = features_selected )
temp2_1 <- run_gams_model_single_run(proc_data,sel_list_vif)

predictions <- as.data.frame(cbind(data_raw$Account,temp1_1$predicted_values))
print(predictions)

t <- temp2_1$predicted_values
t$category <- ifelse(t$predicted<=0.14,"low",ifelse(t$predicted>0.45,"high","moderate"))
temp2_1$predicted_values$category <- t$category 

# run for icu complicaton
proc_data <- gen_proc_data(data_raw,features_selected,data_raw$ICU_comp)
sel_list_vif <- vif_test(data_raw,outcome =data_raw$ICU_comp,feature_list = features_selected )
temp3_1 <- run_gams_model_single_run(proc_data,sel_list_vif)

predictions <- as.data.frame(cbind(data_raw$Account,temp1_1$predicted_values))
print(predictions)

t <- temp3_1$predicted_values
t$category <- ifelse(t$predicted<=0.3,"low",ifelse(t$predicted>0.6,"high","moderate"))
temp3_1$predicted_values$category <- t$category 


# run for 30 day mortality complicaton
proc_data <- gen_proc_data(data_raw,features_selected,data_raw$mort_status_30d)
sel_list_vif <- vif_test(data_raw,outcome =data_raw$ICU_comp,feature_list = features_selected )
temp4_1 <- run_gams_model_single_run(proc_data,sel_list_vif)

predictions <- as.data.frame(cbind(data_raw$Account,temp1_1$predicted_values))
print(predictions)

t <- temp4_1$predicted_values
t$category <- ifelse(t$predicted<=0.04,"low",ifelse(t$predicted>0.15,"high","moderate"))
temp4_1$predicted_values$category <- t$category 

print(t$category)
