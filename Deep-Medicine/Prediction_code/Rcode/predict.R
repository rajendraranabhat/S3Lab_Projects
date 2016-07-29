library(mgcv)
library(verification)
library(VIF)
library(e1071)
library(randomForest)
library(cvTools)

#load models
load(file = "30d.RData")
load(file="mvco.RData")
load(file="icuco.RData")
load(file="cvco.RData")

#load files
    data_raw <- read.csv("C:/Users/Swati/PycharmProjects/RawDataConversion/processeddata.csv",header = TRUE,stringsAsFactors=FALSE)
       cutoff<- read.csv("cutoffs.csv",header = TRUE,stringsAsFactors=FALSE)
    features <- read.csv("M:/IDEALIST/4 IDEALIST Analytic Core/Prediction of PC/Preop Data for Analysis/feature_list.csv",header = TRUE,stringsAsFactors=FALSE)
features_all <- read.csv("M:/IDEALIST/4 IDEALIST Analytic Core/Prediction of PC/Preop Data for Analysis/feature_list_all.csv",header = TRUE,stringsAsFactors=FALSE)
        dict <- data.frame(read.csv("dict_var_final.csv"),stringsAsFactors=FALSE)
      groups <- data.frame(read.csv("groups.csv"),stringsAsFactors=FALSE)

# assign admission types to each patient
t <- ifelse(data_raw$nsaids_adm==1&(data_raw$vanco_adm==1|data_raw$diuret_adm==1|data_raw$aminog_adm==1),2,
            ifelse(data_raw$nsaids_adm==1,1,0))


# create Number of nephrotoxic medications
data_raw$nephtox_adm <- t 
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

#Omit Unnecessary Features
res_prediction <- data.frame(data_raw$acc)
names(res_prediction)[1]<-"Account"
drops <- c('Discharge_date','count_PROTURn', 'cancer','PARA','NEURO','nephtox_adm','acc.1','acc','Check','BLDLOSS',	'ANEMDEF',	'ALCOHOL',	'DRUG',	'frailty_score_all50',	'aki_recov_corr',	'ckd_stage_gr',	'ckd_stage',	'GR_renal5_newest',	'grp8_CORR',	'kdigo_corr',	'aki_kdigo_corr',	'rrt_corr',	'Died',	'icu_days2',	'ICU_comp',	'MV_days',	'MV_comp',	'sepsis',	'septic_shock',	'severe_sepsis',	'postop_inf_new',	'wound_comp_new',	'proc_comp_new',	'cv_comp_new',	'pulm_comp_new',	'vte_new',	'gi_comp_new',	'neurocom_new',	'delirium_new',	'proc_wound_inf',	'neuro_delirium',	'cv_inot_pres',	'ltostatus_new',	'censor',	'mort_status_90d',	'mort_status_30d',	'time',	'ICD_CODE',	'cod_cancer_Gans',	'cod_Cardiovascular_Gans',	'status_cardio_Gans')
data_raw = data_raw[,!(names(data_raw) %in% drops)]

#df$Year_of_admission = 1
feat_num <- features_all[ which(features_all$feature_type =="num"),]
for(i in 1:length(feat_num)){
  ind <- which(colnames(data_raw)==feat_num[i,1])
  if(length(ind)==0){
    print('empty')
    next
  }
  if(length(ind)>1){ind <- ind[1]}
  data_raw[,ind] <- as.numeric(data_raw[,ind])
  
}
  
  
  
#Translating dictionary features
feat_list<-unique(dict$feat_name)
for(i in 1:length(feat_list)) {
    ind <- which(colnames(data_raw)==feat_list[i])
    if(length(ind)==0){
      print('empty')
      next
    }
    if(length(ind)>1){ind <- ind[1]}
    data  <- data.frame(data_raw[,ind],stringsAsFactors = FALSE)
    subst <- dict[ which(dict$feat_name == feat_list[i]),]
    feature_levels<-data.frame(subst,stringsAsFactors = FALSE)
    for (j in 1:nrow(subst)){
      data[which(data[,1]==subst[j,3]),1] <- as.numeric(subst[j,4])
    }
    
    data_raw[,ind] <-data
    data_raw[,ind] <- as.numeric(data_raw[,ind])
}


#Train Procedure lookup
drops <- c("X")
groups = groups[,!(names(groups) %in% drops)]

#Translating procedure variable

data_raw[,ind1] <-procedures
data_raw[,ind1] <- as.numeric(data_raw[,ind1])
limit<-100
ind1<-0
ind1 <- which(colnames(data_raw)=='pr1c')
data <- data_raw[,ind1] 
data <- gsub("[^0-9]","",data)
lowlim<- c(100, 101, 106, 108, 117, 118, 121, 130, 135, 140, 142, 155, 160, 165, 172, 176, 185, 187)
procedures<-rep(0, times = length(data))
for (i in 1:length(data)) {
  flag<-0
  k<-0
  s<-as.character(data[i])
  while (k <= nchar(s) - 2){
    ind<-as.numeric(paste("1", substr(s,1,(nchar(s) - k)),sep = ""))
    
    if (groups[ind,1]+groups[ind,2] >= limit){
      if (groups[ind,1] == 0){
        procedures[i]<-log(1/(2*groups[ind,2]))
      }
      else if (groups[ind,2] == 0){
        procedures[i]<-log(2*groups[ind,1])
      }
      else{
        procedures[i] = log(groups[ind,1]/groups[ind,2]); 
      }
      flag<-1
      break	
    }
    k<-k+1
  }
  if (flag == 0){
    q<-as.numeric(paste("1", substr(s,1,2), sep = ""))
    for (j in (length(lowlim)+1):-1:2){
      if (q >= lowlim[j-1]){
        if (groups[j,1]+groups[j,2] > 0){
          if (groups[j,1] == 0){
            procedures[i]<-log(1/(2*groups[j,2]))
          }
          else if (groups[j,2] == 0){
            procedures[i]<-log(2*groups[j,1])
          }
          else{
            procedures[i] = log(groups[j,1]/groups[j,2]); 
          }
        }
        else{
          if (groups[1,1] == 0){
            procedures[i]<-log(1/(2*groups[1,2]))
          }
          else if (groups[1,2] == 0){
            procedures[i]<-log(2*groups[1,1])
            
          }
          else{
            procedures[i] = log(groups[1,1]/groups[1,2]); 
          }
          
        }
        break
      }
    }
  }
}

data_raw[,ind1] <- as.numeric(procedures)



res_prediction$pred_cv  <- predict(max_auc_model_cvcomp,data_raw,type="response")
res_prediction$cat_cv <- ifelse(res_prediction$pred_cv <= cutoff$cvco[1],"low",
                                   ifelse(res_prediction$pred_cv>cutoff$cvco[2],"high","moderate"))

res_prediction$pred_mv  <- predict(max_auc_model_mvcomp,data_raw,type="response")
res_prediction$cat_mv <- ifelse(res_prediction$pred_mv <= cutoff$mvco[1],"low",
                                ifelse(res_prediction$pred_mv>cutoff$mvco[2],"high","moderate"))

res_prediction$pred_icu <- predict(max_auc_model_ICU_comp,data_raw,type="response")
res_prediction$cat_icu <- ifelse(res_prediction$pred_icu <= cutoff$icuco[1],"low",
                                ifelse(res_prediction$pred_icu>cutoff$icuco[2],"high","moderate"))

res_prediction$pred_30d <- predict(max_auc_model_mort_status_30d,data_raw,type="response")
res_prediction$cat_30d<- ifelse(res_prediction$pred_30d <= cutoff$mort_30d[1],"low",
                                ifelse(res_prediction$pred_30d>cutoff$mort_30d[2],"high","moderate"))

write.csv(res_prediction,"risk_prediction.csv")

