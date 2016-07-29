############################################################################################
# Created by Paul Thottakkara : Last Updated on 17 june 2016 by Ashkan Ebadi & Shivam Mittal
# 
# This is th main file which has two sections, 1st section is the Read Data file that reads
# the user defined functions and data required. 2nd Section will pre-process the raw - data
# and generate the best GAM-Model and classify the different patients into high,medium
# & low categories by selecting the cutoff parameters for each complication
#
# Required files for running this functions are:-
#  *Data_Analysis.R
#  *PreProcessing.R
#  *Model_Build_Validation.R
#  *Metric_Evaluation.R 
# This file contains the user defined functions for processing the data and building the model
############################################################################################


# libraries required
library(mgcv)
library(verification)
library(VIF)
library(e1071)
library(randomForest)
library(cvTools)

# Include User-Defined Fucntions
source("PreProcessing.R") 
source("Model_Build_Validation.R")
source("Data_Analysis.R")
source("Metric_Evaluation.R")

# This is the Read Data file that reads the user defined functions and data required. 
######
# This reads data from three diffrent files namely:-
# "data_raw" consists of entire cohort patient information icnluding both geographical and medical features
# "features" file contains name of important features and its corresponding data type like AGE:integer
# "features_all" contains names of every feature present in the cohort database
######
# It also perform basic pre-processing of data based on different medical conditions

# read all the required data files 

data_raw <- read.csv("data_11_26_2015_116vars_ordered_clean.csv",header = TRUE)
features <- read.csv("feature_list.csv",header = TRUE)
features_all <- read.csv("feature_list_all.csv",header = TRUE)

# assign admission types to each patient
t <- ifelse(data_raw$nsaids_adm==1&(data_raw$vanco_adm==1|data_raw$diuret_adm==1|data_raw$aminog_adm==1),2,
            ifelse(data_raw$nsaids_adm==1,1,0))

data_raw$nephtox_adm <- t 

# create Number of nephrotoxic medications
ind <- which(colnames(data_raw)%in%c("aminog_adm","diuret_adm","vanco_adm","ace_adm","nsaids_adm","inot_pres_adm"))
no_nephrotoxic_meds <- rowSums(data_raw[,ind],na.rm = T)
data_raw$no_nephrotoxic_meds <- no_nephrotoxic_meds

# grouping Urine Protein
t <- ifelse(data_raw$max_PROTUR_gr2==">=300",2,ifelse(data_raw$max_PROTUR_gr2=="TR-30-100",1,0))
data_raw$max_PROTUR_gr2 <- as.factor(t)

# grouping urinal hemoglobin
t <- ifelse(data_raw$max_HGBUR_gr=="Large",2,ifelse(data_raw$max_HGBUR_gr=="Missing"|data_raw$max_HGBUR_gr=="NEGATIVE",0,1))
data_raw$max_HGBUR_gr <- as.factor(t)

# grouping urinal glucose
t <- ifelse(data_raw$max_GLUURN_gr=="Large",2,ifelse(data_raw$max_GLUURN_gr=="Missing"|data_raw$max_GLUURN_gr=="NEGATIVE",0,1))
data_raw$max_GLUURN_gr <- as.factor(t)

# grouping of No of complete blood count tests
t <- ifelse(data_raw$count_HGBn==0,0,ifelse(data_raw$count_HGBn==1,1,"2 or more"))
data_raw$count_HGBn <- t

#End of Reading Data
###############################################################################################

features_selected <- features_all[-c(38,51,52,73,74),]
# run for CV complication
proc_data <- gen_proc_data(data_raw,features_selected,data_raw$cv_comp_new)
sel_list_vif <- vif_test(data_raw,outcome =data_raw$cv_comp_new,feature_list = features_selected )
kfold_allModels_cvcomp <- gen_gam_model_kfold(proc_data,sel_list_vif)

## get the best model based on highes auc                        
max_auc_model_cvcomp <- kfold_allModels_cvcomp$models[[(which.max(kfold_allModels_cvcomp$results[,8])-1)/99]]

## run the best model on the entire dataset
data_new_cvcomp <- proc_data
data_new_cvcomp$cvcomppred <- predict(max_auc_model_cvcomp,data_new_cvcomp,type="response") ; 
metric_cvcomp <-  calculate_metric(data_new_cvcomp$outcome,data_new_cvcomp$cvcomppred) 
cutoff1_cvcomp <- metric_cvcomp[which.max(metric_cvcomp[,7]),1]
cutoff2_cvcomp <- calculate_cutoff2(metric_cvcomp[,1:2])
##plot_roc(metric_cvcomp[,5],metric_cvcomp[,6],metric_cvcomp[,1],metric_cvcomp[1,8],cutoff1,cutoff2)
data_new_cvcomp$category <- ifelse(data_new_cvcomp$cvcomppred<=cutoff1_cvcomp,"low",
                              ifelse(data_new_cvcomp$cvcomppred>cutoff2_cvcomp,"high","moderate"))

#write.csv(metric_cvcomp,"cvcomp-nwa.csv")
write.csv(data_new_cvcomp[,c('cvcomppred','outcome','category')],"cvcomp_result.csv")

# run for MV complication
proc_data <- gen_proc_data(data_raw,features_selected,data_raw$MV_comp)
sel_list_vif <- vif_test(data_raw,outcome =data_raw$MV_comp,feature_list = features_selected )
kfold_allModels_mvcomp <- gen_gam_model_kfold(proc_data,sel_list_vif)
## get the best model based on highest auc                        
max_auc_model_mvcomp <- kfold_allModels_cvcomp$models[[(which.max(kfold_allModels_cvcomp$results[,8])-1)/99]]

## run the best model on the entire dataset
data_new_mvcomp <- proc_data
data_new_mvcomp$mvcompppred <- predict(max_auc_model_mvcomp,data_new_mvcomp,type="response") ; 
metric_mvcomp <-  calculate_metric(data_new_mvcomp$outcome,data_new_mvcomp$mvcompppred) 
cutoff1_mvcomp <- metric_mvcomp[which.max(metric_mvcomp[,7]),1]
cutoff2_mvcomp <- calculate_cutoff2(metric_mvcomp[,1:2])
##plot_roc(metric_cvcomp[,5],metric_cvcomp[,6],metric_cvcomp[,1],metric_cvcomp[1,8],cutoff1,cutoff2)
data_new_mvcomp$category <- ifelse(data_new_mvcomp$mvcompppred<= cutoff1_mvcomp,"low",
                              ifelse(data_new_mvcomp$mvcompppred>cutoff2_mvcomp,"high","moderate"))
#write.csv(metric_mvcomp,"mvcomp-nwa.csv")
write.csv(data_new_mvcomp[,c('mvcompppred','outcome','category')],"mvcomp_res.csv")

# run for ICU complication
proc_data <- gen_proc_data(data_raw,features_selected,data_raw$ICU_comp)
sel_list_vif <- vif_test(data_raw,outcome =data_raw$ICU_comp,feature_list = features_selected )
kfold_allModels_icucomp <- gen_gam_model_kfold(proc_data,sel_list_vif)
max_auc_model_ICU_comp <- kfold_allModels_icucomp$models[[(which.max(kfold_allModels_icucomp$results[,8])-1)/99]]

## run the best model on the entire dataset
data_new_ICU_comp <- proc_data
data_new_ICU_comp$ICU_comppred <- predict(max_auc_model_ICU_comp,data_new_ICU_comp,type="response") ; 
metric_ICU_comp <-  calculate_metric(data_new_ICU_comp$outcome,data_new_ICU_comp$ICU_comppred) 
cutoff1_ICU_comp <- metric_ICU_comp[which.max(metric_ICU_comp[,7]),1]
cutoff2_ICU_comp <- calculate_cutoff2(metric_ICU_comp[,1:2])
##plot_roc(metric_cvcomp[,5],metric_cvcomp[,6],metric_cvcomp[,1],metric_cvcomp[1,8],cutoff1,cutoff2)
data_new_ICU_comp$category <- ifelse(data_new_ICU_comp$ICU_comppred<=cutoff1_ICU_comp,"low",
                                ifelse(data_new_ICU_comp$ICU_comppred>cutoff2_ICU_comp,"high","moderate"))
#write.csv(metric_ICU_comp,"icucomp.csv")
write.csv(data_new_ICU_comp[,c('ICU_comppred','outcome','category')],"icucomp_res.csv")


# run for 30 day mortality
proc_data <- gen_proc_data(data_raw,features_selected,data_raw$mort_status_30d)
sel_list_vif <- vif_test(data_raw,outcome =data_raw$mort_status_30d,feature_list = features_selected )
kfold_allModels_30dMort <- gen_gam_model_kfold(proc_data,sel_list_vif)
max_auc_model_mort_status_30d <- kfold_allModels_30dMort$models[[(which.max(kfold_allModels_30dMort$results[,8])-1)/99]]

data_new_mort_status_30d <- proc_data
data_new_mort_status_30d$mort_status_30dpred <- predict(max_auc_model_mort_status_30d,data_new_mort_status_30d,type="response") ; 
metric_mort_status_30d <-  calculate_metric(data_new_mort_status_30d$outcome,data_new_mort_status_30d$mort_status_30dpred) 
cutoff1_mort_status_30d <- metric_mort_status_30d[which.max(metric_mort_status_30d[,7]),1]
cutoff2_mort_status_30d <- calculate_cutoff2(metric_mort_status_30d[,1:2])
##plot_roc(metric_cvcomp[,5],metric_cvcomp[,6],metric_cvcomp[,1],metric_cvcomp[1,8],cutoff1,cutoff2)
data_new_mort_status_30d$category <- ifelse(data_new_mort_status_30d$mort_status_30dpred<=cutoff1_mort_status_30d,"low",
                                      ifelse(data_new_mort_status_30d$mort_status_30dpred>cutoff2_ICU_comp,"high","moderate"))

#write.csv(metric_mort_status_30d,"30d-metric-bestmodel.csv")
write.csv(data_new_mort_status_30d[,c('mort_status_30dpred','outcome','category')],"30d-prediction-category.csv")

##END