############################################################################################
# Created by Paul Thottakkara : Last Updated on 17 june 2016 by Ashkan Ebadi & Shivam Mittal
# 
# This file contains all set of functions used for pre-processing the raw data before it is
# used to generate GAM-models and predict probabilities of the patient using the best model.
# 
# The Different Functions in this file are:-
#    *gen_proc_data
#    *train_categorical_feature
#    *train_procedure_feature
#    *outlier_detect
#    *clean_categorical
#    *vif_test
############################################################################################

############
# Function Input:-    Table containing Metric for each threshold value
# Function Output:-   Return the cutoff-2 threshold value for the input metric data
#                   
# Function Used:-     None
# Function Purpose:-  Used to evaluate cutoff2 by checking the plateau of the 
#                     accuracy curve
############

calculate_cutoff2<- function(data)
{
  val<-0
  for(i in 1:(nrow(data)-10))
  {
    # change in accuracy is less than 0.2% in next 10 consecutive threshold values
    if((abs(data[i,2]-data[i+10,2]))<0.002)
    {
      val<-data[i,1]
      break;
    }
  }
  return(val)
}


############
# Function Input:-    1> obsereved ouctome data column 
#				      2> predicted score from GAM model
#                     3> Threshold value
# Function Output:-   List containing value  Accuracy, Positive Predicted value
#                     Negative Predicted value, Specivity,Sensitivity,
#                     yoden index
#                   
# Function Used:-     None
# Function Purpose:-  calculates all the metric values using threshold value to
#                     classify it as positive or negative outcome
############
ROC_parameters <- function(obser,score,thr){
  temp <- rep(0,length(score)) ; temp[which(score>=thr)] <- 1
  p_ind <- which(obser==1) ; n_ind <- which(obser==0)
  TP <- sum(temp[p_ind]==1) ; FP <- sum(temp[n_ind]==1)
  TN <- sum(temp[n_ind]==0) ; FN <- sum(temp[p_ind]==0)
  acc <- (TP+TN)/length(temp)
  ppv <- TP/(TP+FP) ; npv <- TN/(TN+FN)
  sen <- TP/(TP+FN) ; spe <- TN/(TN+FP)
  yod <- sen+spe-1
  
  return(list("acc"=acc,"ppv"=ppv,"npv"=npv,"sen"=sen,"spe"=spe,"yod"=yod))
  
}


############
# Function Input:-    1> obsereved ouctome data column 
#				      2> predicted score from GAM model
#
# Function Output:-   List containing value  Accuracy, Positive Predicted value
#                     Negative Predicted value, Specivity,Sensitivity,
#                     yoden index for every thershold value from 0.01 to 0.99
#
# Function Used:-     ROC_parameters()
#
# Function Purpose:-  calculates all the metric values for every threshold value
#                     ranging from 0.01 to 0.99 and
#                     classify it as positive or negative outcome
############
calculate_metric<- function(outcome, pred){
  obser <- rep(0,times = length(outcome))
  obser[which(outcome==1)] <- 1 ; obser <- as.numeric(obser)
  score <- as.numeric(pred)
  prev <- round(sum(obser)/length(obser),digits=2)
  thres <- seq(0.01,1,length.out=100) ; thres <- thres[-c(100)]
  xval <- thres
  acc <- array(dim=length(thres))
  ppv <- array(dim=length(thres))
  npv <- array(dim=length(thres))
  sen <- array(dim=length(thres))
  spe <- array(dim=length(thres))
  yod <- array(dim=length(thres))
  auc <- array(dim=length(thres))
  for(l in 1:length(thres)){
    plotdata <- ROC_parameters(obser,score,thres[l])
    acc[l] <- round(plotdata$acc,3)
    ppv[l] <- round(plotdata$ppv,3)
    npv[l] <- round(plotdata$npv,3)
    sen[l] <- round(plotdata$sen,3)
    spe[l] <- round(plotdata$spe,3)
    yod[l] <- round(plotdata$yod,3)
    auc[l] <- round(roc.area(obser,score)$A,4)
  }
  prev <- round(sum(obser)/length(obser),2)
  roc_vals <- data.frame(matrix(nrow=length(spe),ncol=8)) ; colnames(roc_vals) <- c("thres","acc","ppv","npv","specificity","sensitivity","yod_index","auc")
  roc_vals[,1] <- thres ; roc_vals[,2] <- acc ; roc_vals[,3] <- ppv
  roc_vals[,4] <- npv; roc_vals[,5] <- spe; roc_vals[,6] <- sen; roc_vals[,7] <- yod;
  roc_vals[,8] <- auc;
  return(roc_vals)
}
