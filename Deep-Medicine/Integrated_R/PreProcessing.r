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
# Function Input:- 1> Feature Column values having categorical data  
#				   2> Outcome column for the complication
#                  3> Limit defining a number used for evaluating statistical importance
#                  4> Number of clusters
# Function Output:- List containing mapping of each categorical and its
#                   corresponding log transformation 
#                   
# Function Used:- None
# Function Purpose:-  Converting individual categorical type to number
#                     to be used on training & test data for evaluating 
#					  patient risk probabilities and building GAM-model
############
train_categorical_feature <- function(categorical_feature, outcome, limit, clusters){
  if (length(unique(categorical_feature)) == 2){
    vocabulary = unique(categorical_feature)
    p  <-  c(0,1)
    d<-rep(0, length(categorical_feature))
    d[categorical_feature == vocabulary[2]] = 1      
    return(list("d" = d, "vocabulary" = vocabulary, "p" = p))
  }	
  cl_vocabulary<-NULL
  cl_p<-NULL	
  vocabulary1<-unique(categorical_feature) 	
  # storing count of outcome 0 & 1 for each categorical type
  count1<-rep(0, times  = length(vocabulary1))
  count2<-rep(0, times  = length(vocabulary1))	
  for (i in 1:length(vocabulary1)){
    if (is.na(vocabulary1[i])){
      count1[i]<-sum((is.na(categorical_feature))*(outcome==1))
      count2[i]<-sum((is.na(categorical_feature))*(outcome==0))
    } else{
      count1[i]<-sum((categorical_feature[!is.na(categorical_feature)] == vocabulary1[i])*(outcome[!is.na(categorical_feature)] == 1))
      count2[i]<-sum((categorical_feature[!is.na(categorical_feature)] == vocabulary1[i])*(outcome[!is.na(categorical_feature)] == 0))}
  }
  condition<-(count1+count2>=limit)
  condition[which(is.na(vocabulary1))]<-TRUE	
  index<-sum(condition)
  vocabulary<-(1:index)
  p<-rep(0, times  = length(vocabulary))
  index<-0
  for (i in (1:length(vocabulary1))){
    if (count1[i]+count2[i]>=limit || is.na(vocabulary1[i])){
      index<-index+1
      vocabulary[index]<-as.character(vocabulary1[i])
      if (count1[i] ==0 )
        p[index]<-log(1/(2*count2[i]))
      else if (count2[i] == 0)
        p[index]<-log(2*count1[i])
      else
        p[index]<-log(count1[i]/count2[i])
    }
  } 
  if (sum(condition==0)<=1){
    if (sum(condition==0) == 1){
      index<-index+1
      if (count1[which(condition==0)] ==0 )
        p[index]<-log(1/(2*count2[which(condition==0)]))
      else if (count2[which(condition==0)] == 0)
        p[index]<-log(2*count1[which(condition==0)])
      else
        p[index]<-log(count1[which(condition==0)]/count2[which(condition==0)])
      vocabulary[index]<-as.character(vocabulary1[which(condition==0)])
    }
  } else{
    cl<-min(clusters, sum(condition == 0)-1)
    residual1<-count1[condition == 0]
    residual2<-count2[condition == 0]
    s<-matrix(rep(0, times = length(residual1)), ncol = 1)
    for (i in 1:length(residual1)){
      if (residual1[i] ==0 )
        s[i]<-log(1/(2*residual2[i]))
      else if (residual2[i] == 0)
        s[i]<-log(2*residual1[i])
      else
        s[i]<-log(residual1[i]/residual2[i])
    }
    v<-kmeans(s, cl)
    for (i in (1:cl)){
      idx1<-(1:length(condition))[condition == 0]
      cl_vocabulary<-data.frame(matrix(nrow = sum(condition == 0), ncol = 2))
      cl_vocabulary[,1]<-as.character(vocabulary1[condition == 0])
      cl_vocabulary[,2]<-v$cluster			
      c1<- count1[idx1[v$cluster == i]]
      c2<- count2[idx1[v$cluster == i]]
      if (sum(c1) ==0 )
        cl_p[i]<-log(1/(2*sum(c2)))
      else if (sum(c2) == 0)
        cl_p[i]<-log(2*sum(c1))
      else
        cl_p[i]<-log(sum(c1)/sum(c2))
    }
  }
  d<-rep(0, times = length(categorical_feature))
  d[is.na(categorical_feature)]<-p[which(is.na(vocabulary))] 
  for (i in 1:length(vocabulary))
    d[categorical_feature==vocabulary[i]]<-p[i]
  if(!is.null(cl_vocabulary)){
    for (i in 1:nrow(cl_vocabulary))
      d[categorical_feature==cl_vocabulary[i,1]]<-cl_p[cl_vocabulary[i,2]]
  }
  output<-list("d" = d, "vocabulary" = vocabulary, "cl_vocabulary" = cl_vocabulary, "p" = p, "cl_p" = cl_p)
}



############
# Function Input:- 1> Feature Column values having procedures data  
#				   2> Outcome column for the complication
#                  3> Limit defining a number used for evaluating statistical importance
#             
# Function Output:- List containing mapping of each procedures and its
#                   corresponding log transformation 
#                   
# Function Used:- None
# Function Purpose:-  Converting individual procedures type to number
#                     to be used on training & test data for evaluating 
#					  patient risk probabilities and building GAM-model
## used to handle the pr1 feature (the procedures followed), 
## network pruned to generate levels that has statistical significance
############
train_procedure_feature <-function(data, outcome, limit){
  lowlim<- c(100, 101, 106, 108, 117, 118, 121, 130, 135, 140, 142, 155, 160, 165, 172, 176, 185, 187)
  procedures<-rep(0, times = length(data))
  groups<-data.frame(matrix(rep(0, times = 20000*2),ncol = 2))
  
  for (i in 1:length(data)){
    if (is.na(data[i]))
      data[i]<-"00"  
    s<-as.character(data[i])
    for (k in nchar(s):-1:2){
      j<-as.numeric(paste("1", substr(s,1,k), sep = ""))
      if (outcome[i] == 1)
        groups[j,1]<-groups[j,1]+1
      else
        groups[j,2]<-groups[j,2]+1		
    }
    num<-as.numeric(paste("1", substr(s,1,2), sep = ""))
    for (j in (length(lowlim)+1):-1:2){
      if (num >= lowlim[j-1]){
        if (outcome[i] == 1)
          groups[j,1]<-groups[j,1]+1
        else
          groups[j,2]<-groups[j,2]+1
        break
      }
    }	
  }
  
  for (i in 2:(length(lowlim)+1)){
    if (groups[i,1]+groups[i,2] < limit){
      groups[1,1] = groups[1,1]+groups[i,1];
      groups[1,2] = groups[1,2]+groups[i,2];
      groups[i,1] = 0;
      groups[i,2] = 0;
      
    }
  }
  
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
  output<-list("procedures" = procedures, "groups" = groups)
}






############
# Function Input:-    Feature Column values 
#
# Function Output:-   Preprocessed Column with no invalid entries
#                   
# Function Used:-     grouping_algo().
#
# Function Purpose:-  preprocess the columns by substituting the missing_values like
#                     ["","MISSING","NA","UNKNOWN","_"," ",np.nan] to 'MISSING'
#                     Also update the column values with 'OTHERS' in case the count is
#                     less than the Threshold value
############
clean_categorical <- function(vect){
  ind <- which(is.na(vect)|vect==""|vect=="MISSING"|vect=="NA"|vect=="UNKNOWN"|vect=="-"|vect==" ")
  if(length(ind)>0){levels(vect) <- c(levels(vect),"MISSING");vect[ind]<-"MISSING"}
  vect <- as.factor(vect) ; 
  absent_levels <- levels(vect)[which(!(levels(vect)%in%unique(vect)))]
  if(length(absent_levels)>0){vect <- droplevels(vect,absent_levels)}
  vect <- grouping_algo(vect)
  return(vect)
}



############
# Function Input:-    Feature Column values
#				                
# Function Output:-   Processed Column having 'OTHERS' value for categories having
#                     fewer counts
#                   
# Function Used:-     None
#
# Function Purpose:-  updating individual values of a column to 'OTHERS' 
#                     whose count is less than  the threshold value(50)
############
grouping_algo <- function(vect){
  thres <- 50
  tab <- table(vect) ; ind <- which(tab<thres)
  if(length(ind)>0){
    low_prop <- names(tab)[ind] ; 
	levels(vect) <- c(levels(vect),"OTHERS")
    ind <- which(vect%in%low_prop) ; 
	vect[ind] <- "OTHERS"
    ind <- which(table(vect)>0) ;
	sel_levels <- names(table(vect))[ind]
    vect <- droplevels(vect,sel_levels)
    if(sum(vect=="OTHERS")<thres){
      if(length(unique(vect))==2){return(vect)}
      tab <- sort(table(vect)) ;
	  rep_level <- names(tab)[2]
      vect[which(vect==rep_level)] <- "OTHERS"
      vect <- droplevels(vect,rep_level)
    }
  }
  return(vect)
}


############
# Function Input:-     Numerical Feature Column 
#				        
# Function Output:-    Outliers and Missing numbers are being replaced by mean
#                   
# Function Used:-      None
#
# Function Purpose:-   Removes the outliers by checking its z values
############
outlier_detect <- function(vect){
  median_dev <- mad(vect,na.rm = TRUE) ;
  x_bar <- mean(vect,na.rm = TRUE)
  ind_l <- which(vect<quantile(vect,probs = 0.01,na.rm = T)) ; 
  ind_u <- which(vect>quantile(vect,probs = 0.99,na.rm = T))
  ind <- which(is.na(vect)) ; 
  if(length(ind)>0){vect[ind]<-x_bar}
  zvalue <- abs(0.6745*(vect-x_bar)) ;
  zvalue <- zvalue/median_dev
  ind1 <- which(zvalue>5) ; 
  out_ind <- NULL
  ind <- intersect(ind1,ind_l) ;
  new_vect <- vect
  if(length(ind)>0)
  {
  new_vect[ind] <- runif(length(ind),quantile(vect,probs = 0.005,na.rm = T),quantile(vect,probs = 0.05,na.rm = T)) ; 
  out_ind <- ind
  } 
  ind <- intersect(ind1,ind_u) 
  if(length(ind)>0)
  {
  new_vect[ind] <- runif(length(ind),quantile(vect,probs = 0.95,na.rm = T),quantile(vect,probs = 0.995,na.rm = T)) ; 
  out_ind <- c(out_ind,ind)
  } 
  #print(paste0(length(ind)," outliers replaced "))
  return(list("data"=new_vect,"outlier_index"=out_ind))
}




############
# Function Input:-    1> Unprocessed data which needs to processed
#                     2> Feature Column values having procedures data  
#             
# Function Output:-   List containing mapping of each procedures and its
#                     corresponding log transformation 
#                   
# Function Used:-     outlier_detect(),train_procedure_feature(),train_categorical_feature()
#                     clean_categorical().
#
# Function Purpose:-  Converting individual procedures type to number
#                     to be used on training & test data for evaluating 
#					  patient risk probabilities and building GAM-model
############
gen_proc_data <- function(raw_data,feature_list,outcome){
  t <- rep(0,length(outcome)) ;
  t[outcome==1] <- 1 ; 
  outcome <- t 
  # replace missing values in admission source
  raw_data$Admission_Source[raw_data$Admission_Source==""] <- "outpatient"
  raw_data <- raw_data[,which(colnames(raw_data)%in%feature_list[,1])]
  raw_data$outcome <- t
  
  if(sum(colnames(raw_data)%in%feature_list[,1])!=nrow(feature_list)){
	print("fields mismatch in feature list and raw data, following not found in raw data")
	print(as.character(feature_list[which(!feature_list[,1]%in%colnames(raw_data)),1]))
  }
  
  for(i in 1:nrow(feature_list)){
    ind <- which(colnames(raw_data)==feature_list[i,1])
    if(length(ind)==0)
	{
	print(feature_list[i,1]);
	next
	}
    if(length(ind)>1){ind <- ind[1]}
    if(feature_list[i,2]=="num"){
	  #removes Outliers from the column having numeric data
      temp <- outlier_detect(raw_data[,ind])
      raw_data[,ind] <- temp$data ; 
	  next
    }
    if(feature_list[i,2]=="cat"&feature_list[i,1]=="pr1c"){
      t <- raw_data[,ind] ; 
	  t <- gsub("[^0-9]","",t)
	  #check train_procedure_feature function for details
      d<-train_procedure_feature(t, outcome, 100)
      raw_data[,ind] <- d$procedures ; next
    }
    if(feature_list[i,2]=="cat"&length(unique(raw_data[,ind]))>5){
	  #check train_categorical_feature function for details
      d<-train_categorical_feature(raw_data[,ind], outcome, 100, 2)          
      raw_data[,ind] <- d$d	; next
    }else{
      raw_data[,ind] <- clean_categorical(raw_data[,ind])
    }
  }
  
  return(raw_data)
}




############
# Function Input:-    1> Unprocessed Raw Data
#				      2> Outcome column for the complication
#                     3> Feature list having name of all features and its corresponding type.
#             
# Function Output:-   Important set of feature from the feature_list having less Variation
#                   
# Function Used:-     outlier_detect(),train_procedure_feature(),train_categorical_feature()
#                     clean_categorical().
#
# Function Purpose:-  Pre-Process the data & Perform VIF Test on it to findout the 
#                     non-collinear features
############
vif_test <- function(raw_data,outcome,feature_list){
  t <- rep(0,length(outcome)) ; t[outcome==1] <- 1 ; outcome <- t 
  # replace missing values in admission source
  raw_data$Admission_Source[raw_data$Admission_Source==""] <- "outpatient"
  raw_data <- raw_data[,which(colnames(raw_data)%in%feature_list[,1])]
  
  if(sum(colnames(raw_data)%in%feature_list[,1])!=nrow(feature_list)){
    print("fields mismatch in feature list and raw data, following not found in raw data")
    print(as.character(feature_list[which(!feature_list[,1]%in%colnames(raw_data)),1]))
    print("execution terminated")
    return(NULL)
  }
  
  for(i in 1:nrow(feature_list)){
    ind <- which(colnames(raw_data)==feature_list[i,1])
    if(length(ind)==0){print(feature_list[i,1]);next}
    if(length(ind)>1){ind <- ind[1]}
    if(feature_list[i,2]=="num"){
      temp <- outlier_detect(raw_data[,ind])
      raw_data[,ind] <- as.numeric(temp$data) ; next
    }
    if(feature_list[i,2]=="cat"&feature_list[i,1]=="pr1c"){
      t <- raw_data[,ind] ; t <- gsub("[^0-9]","",t)
      d<-train_procedure_feature(t, outcome, 100) ; rm(t)
      raw_data[,ind] <- as.numeric(d$procedures) ; next
    }else{
      t <- clean_categorical(raw_data[,ind])
      d<-train_categorical_feature(t, outcome, 100, 2)  ; rm(t)        
      raw_data[,ind] <- as.numeric(d$d)	;
    }
  }
  
  x <- raw_data[,which(colnames(raw_data)%in%feature_list[,1])]
  y <- outcome
  t <- vif(y,x,mode="dense",trace = F,subsize = round(0.6*length(y),0))
  selected_feat <- feature_list[t$select,]
  return(selected_feat)
  
}


