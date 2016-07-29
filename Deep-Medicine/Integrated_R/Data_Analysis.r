############################################################################################
# Created by Paul Thottakkara : Last Updated on 17 june 2016 by Ashkan Ebadi & Shivam Mittal
# 
# This file contains all set of functions used for performing various data analysis on the 
# dataset and deduce various inferences by performing statistical analysis on the data
# 
# The Different Functions in this file are:-
#    *univ_analysis
#    *variable_sum
#    *create_summary_table
#    *create_table2
############################################################################################


########
# Perfoming analysis using univariate models
# Function Input:- raw_data and feature_list 
# Function Output:- Result of Univarte Analysis 
# Function Purpose:- calculates the z-value and p-value of each feature from the feature_list
#########

univ_analysis <- function(model_data,feat_all){
  fm<-binomial();  fm$link = "logit";
  p_ind <- which(model_data$outcome==1) ; 
  n_ind <- which(model_data$outcome==0) 
  rest_uni <- data.frame(matrix(nrow=nrow(feat_all),ncol=4))
  colnames(rest_uni) <- c("Variable","Z_val_Log_Reg","P_val_Log","P_val_t_test")
  for(i in 1:nrow(feat_all)){
    rest_uni[i,1] <- as.character(feat_all[i,1]) ; print(i)
    ind <- which(colnames(model_data)==feat_all[i,1])
    s <- as.formula(paste("outcome~",feat_all[i,1]))
    model_temp <- glm(formula = s,family = fm,data=model_data) ; sm <- summary(model_temp)
	# Calculates the coefficients for Numerical feature type
    if(feat_all[i,2]=="num"){
      # z value and p value
      rest_uni[i,2] <- round(sm$coefficients[2,3],1) ; 
	  rest_uni[i,3] <- round(sm$coefficients[2,4],3) 
      t_test <- t.test(model_data[p_ind,ind],model_data[n_ind,ind])
      rest_uni[i,4] <- round(t_test$p.value,3)
    }
	# Calculates the values for Categorical data having Unique Categories count >5
	else if(length(unique(model_data[,ind]))>5){
      # z value and p value
      rest_uni[i,2] <- round(sm$coefficients[2,3],1) ;
	  rest_uni[i,3] <- round(sm$coefficients[2,4],3) 
      t_test <- t.test(model_data[p_ind,ind],model_data[n_ind,ind])
      rest_uni[i,4] <- round(t_test$p.value,3)
    }else{
      rest_uni[i,2]  <- paste(round(sm$coefficients[-1,3],3),collapse = ",")
      rest_uni[i,3]  <- paste(round(sm$coefficients[-1,4],3),collapse = ",")
    }
  }
  return(rest_uni)
}


########
# Perfoming analysis using univariate models
# Function Input:- 1> Data Column
#                  2> Type of the data on that particular column
#                  3> Name of the Column feature
# Function Output:- Mean, count, Medain, Percentile of the data
# Function Used:- None
# Function Purpose:- Used by create_summary_table() to create the
#                    dataset summary table 
#########
variable_sum <- function(var,type,var_name){
  output1 <- data.frame(matrix(nrow=1,ncol=5)) ; 
  colnames(output1) <- c("var_name","var_type","sum_Stat","Ref","Missing")
  if(type=="cat"){
    if(length(unique(var))==2){
      l <- levels(factor(var)) ;
	  output1$Ref <- l[1] ; 
	  output1$var_name <- paste(var_name,": ",l[2],sep = "") ;
	  output1$var_type <- type ; 
      c <- sum(var==l[2]) ; 
	  p <- round(100*c/length(var),1) ;
	  output1$sum_Stat <- paste(c," (",p,")",sep="") ;
	  output1$Missing <- sum(is.na(var)|var==""|var=="NA")
    }
    if(length(unique(var))<=5 & length(unique(var))>2 ){
      l <- levels(factor(var)) 
      output1 <- data.frame(matrix(nrow=length(l)+1,ncol=4)) ;
	  colnames(output1) <- c("var_name","var_type","sum_Stat","Ref")
      output1$Ref[1] <- l[1] ; output1$var_name[1] <- as.character(var_name) ; 
	  output1$var_type[1] <- as.character(type) ; 
	  output1$sum_Stat[1] <- "n(%)"
      output1$Missing[1] <- sum(is.na(var)|var==""|var=="NA")
      for(i in 1:length(l)){
        c <- sum(var==l[i]) ; 
		p <- round(100*c/length(var),1) ; 
		output1$sum_Stat[i+1] <- paste(c," (",p,")",sep="") ; 
		output1$var_name[i+1] <- l[i]
      }
    }
    if(length(unique(var))>5){
      tab <- sort(table(var),decreasing = TRUE)
      output1 <- data.frame(matrix(nrow=6,ncol=4)) ; 
	  colnames(output1) <- c("var_name","var_type","sum_Stat","Ref")
      output1$var_name[1] <- as.character(var_name) ; 
	  output1$var_type[1] <- as.character(type) ;
	  output1$Ref[1] <- ">5 levels" ; output1$sum_Stat[1] <- "n(%)"
      output1$Missing[1] <- sum(is.na(var)|var==""|var=="NA")
      for(i in 1:5){
        c <- tab[i] ; p <- round(100*c/length(var),1) ; 
		output1$sum_Stat[i+1] <- paste(c," (",p,")",sep="") ; 
		output1$var_name[i+1] <- names(tab[i])
      }
    }
  }
  if(type=="num"){
    rnd=1
    output1$var_name[1] <- as.character(var_name) ; 
	output1$var_type[1] <- as.character(type) ;
	m <- round(median(var,na.rm = TRUE),rnd) ; 
    qt1 <- round(quantile(var,probs = 0.25,na.rm = TRUE),rnd) ; 
	qt2 <- round(quantile(var,probs = 0.75,na.rm = TRUE),rnd)
    output1$sum_Stat[1] <- paste(m," (",qt1,",",qt2,")",sep = "")
    output1$Missing[1] <- sum(is.na(var)|var==""|var=="NA")
  }
  return(output1)
}


######
# Function Input:- raw_data and feature_list 
# Function Output:- Detailed Report on Feature,its type,mean-value,range,
#                   count of Unique category for Categorical feature
#                   count of Missing values for each feature
# Function Used:- variable_sum
# Function Purpose:- Summarizes the Cohort Dataset
#########

create_summary_table <- function(data,features_sel){
  tab_output <- NULL ; 
  for(i in 1:nrow(features_sel)){
    print(as.character(features_sel$feature_name[i]))
    var <- data[,which(colnames(data)==features_sel$feature_name[i])] ;
    var_name <- features_sel$feature_name[i] ; type <- features_sel$feature_type[i]
    tab_output <- rbind(tab_output,variable_sum(var,type,var_name))
  }
  return(tab_output)
  
}


########
# Function Input:- Model Coefficients
# Function Output:- Table having odd-ratio & Confidence interval
# Function Used:- None
# Function Purpose:- Used to calculate odd-ratio and its correspodning CI
#########

create_table2 <- function(model){
  # Results for Table 2 (Odds ratio for the variables in the model)
  ods <- round(exp(coef(model)),2) ; 
  odd_ci <- exp(confint.default(model,level=0.99)) ; 
  ci_ll <- round(odd_ci[,1],2) ; ci_ul <- round(odd_ci[,2],2)
  ci <- paste("(",ci_ll," , ",ci_ul,")",sep="")       
  table2 <- cbind(ods,ci) ; 
  colnames(table2) <- c("Odds_Ratio","Odds_Ratio_CI_99%")
  return(table2)
}


