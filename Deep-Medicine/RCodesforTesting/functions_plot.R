# Function used for the main  file for plotting

# Performance parameters (ROC and related)
plot_perform <- function(outcome, pred,cut1,cut2,x_lab,heading){
  obser <- rep(0,times = length(outcome))
  obser[which(outcome==1)] <- 1 ; obser <- as.numeric(obser)
  score <- as.numeric(pred)
  #roc_area <- roc.area(obser,score)
  #roc.plot(obser,score,main=paste("ROC curve, AUC:",round(roc_area$A,digits=2),sep=""))
  prev <- round(sum(obser)/length(obser),digits=2)
  thres <- seq(0.01,max(score),length.out=100) ; thres <- thres[-c(99,100)]
  xval <- thres
  acc <- array(dim=length(thres))
  ppv <- array(dim=length(thres))
  npv <- array(dim=length(thres))
  sen <- array(dim=length(thres))
  spe <- array(dim=length(thres))
  yod <- array(dim=length(thres))
  for(l in 1:length(thres)){
    plotdata <- ROC_parameters(obser,score,thres[l])
    acc[l] <- round(plotdata$acc,3)
    ppv[l] <- round(plotdata$ppv,3)
    npv[l] <- round(plotdata$npv,3)
    sen[l] <- round(plotdata$sen,3)
    spe[l] <- round(plotdata$spe,3)
    yod[l] <- round(plotdata$yod,3)
  }
  prev <- round(sum(obser)/length(obser),2)
  x_name <- paste("Predicted Risk",x_lab,sep="")
  plot(xval,acc,xlim=c(0,1),ylim=c(0,1),xlab=x_name,ylab="Performance measures",type="l",lwd=2,main=heading,cex=0.8)
  lines(xval,ppv,col="green",lty=1,lwd=2) ; lines(xval,npv,col="red",lty=1,lwd=2) 
  lines(xval,yod,col="blue",lty=1,lwd=2)
  lines(rep(cut1,times=10),seq(0,1,length.out = 10),lty=3) ; lines(rep(cut2,times=10),seq(0,1,length.out = 10),lty=5)
  legend("bottomright",legend=c("Accuracy","PPV","NPV","Youden Index"),col=c("black","green","red","blue"),lty=c(1,1,1,1),lwd=c(2,2,2,2),bty="n",cex=0.8)
  legend("bottomleft",legend=c(paste("Cutoff1: ",cut1,sep=""),paste("Cutoff2: ",cut2,sep="")),lty=c(3,5),bty="n",cex=0.85)
  roc_vals <- data.frame(matrix(nrow=length(spe),ncol=3)) ; colnames(roc_vals) <- c("specificity","sensitivity","thres")
  roc_vals[,1] <- spe ; roc_vals[,2] <- sen ; roc_vals[,3] <- thres
  return(roc_vals)
}

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

roc_area_fun <- function(model_data,lim_dof=NULL,feat_sel,s_index,rep,cut1,cut2){
  if(is.null(lim_dof))
    lim_dof=10
  s <- "outcome~" ; fm<-binomial();  fm$link = "logit";
  for(i in 1:nrow(feat_sel)){
    if(i %in% s_index){
      s <- paste(s,"s(",feat_sel[i,1],",k=",lim_dof,")+",sep="")
      
    }else {
      s <- paste(s,feat_sel[i,1],"+",sep="")
    }
  } 
  s <- substr(s,1,nchar(s)-1) ; s <- as.formula(s)
  
  roc_res <- data.frame(matrix(nrow=rep,ncol=6)) ; colnames(roc_res) <- c("AUC","HL","Spe_1","Sen_1","Spe_2","Sen_2")
  for(i in 1:rep){
    print(i)
    
    train_ind <- sample(1:nrow(model_data),size = floor(0.7*nrow(model_data)))
    test_ind <- setdiff(1:nrow(model_data),train_ind)
    train_data <- model_data[train_ind,] ; test_data <- model_data[test_ind,]
    
    model <- bam(s, data = train_data, family = fm)
    pred <- predict(model,newdata = test_data,type="response")
    temp <- rep(0,nrow(test_data)) ; temp[which(test_data$outcome==1)] <- 1
    auc <- round(roc.area(temp,pred)$A,3) ; HL <- round(hosmerlem(y = temp,yhat = pred)$p,3)
    roc_res[i,1] <- auc ; roc_res[i,2] <- HL
    spe_sen1 <- ROC_parameters(temp,pred,cut1) ; spe_sen2 <- ROC_parameters(temp,pred,cut2)
    roc_res[i,3] <- round(spe_sen1$spe,3) ;     roc_res[i,4] <- round(spe_sen1$sen,3)
    roc_res[i,5] <- round(spe_sen2$spe,3) ;     roc_res[i,6] <- round(spe_sen2$sen,3)
  }
  return(roc_res)
  
}

plot_roc <- function(spe,sen,thres,auc_vect,cut1,cut2){
  cut1_ind <- which(abs(thres-cut1)==min(abs(thres-cut1))) ; cut2_ind <- which(abs(thres-cut2)==min(abs(thres-cut2)))
  m <- round(mean(auc_vect,na.rm = TRUE),3)
  std <- round(sd(auc_vect,na.rm = TRUE),3)
  auc <- paste("AUC = ",m," (",round(m-1.96*std,3),",",round(m+1.96*std,3),")",sep="")
  plot(1-spe,sen,xlab="1-Specificity",ylab="Sensitivity",xlim=c(0,1),ylim=c(0,1),type="l",lwd=2)
  
  x1 <- c(1-spe[cut1_ind],1-spe[cut2_ind]) ; y1 <- c(sen[cut1_ind],sen[cut2_ind])
  points(x1,y1,pch=15)
  cutoffs <- c(paste("Cutoff1 (",round(thres[cut1_ind],2),")",sep=""),paste("Cutoff2 (",round(thres[cut2_ind],2),")",sep=""))
  text(x1+0.01,y1-0.01,cutoffs,pos=4)
  text(0.6,0.2,auc,pos=4)
}

# functio to compare models using nri, cfnri and idi
nri_idi_values <- function(old_model,new_model,rep,cutoff){
  s_o <- as.formula(old_model$formula) ; s_n <- as.formula(new_model$formula)
  data_old <- old_model$model ; data_new <- new_model$model
  if(nrow(data_old)!=nrow(data_new))
    print("both models cannot be compared, mismatch in size")
  outcome <- rep(0,times = nrow(data_old)) ; outcome[which(data_old$outcome==1)] <- 1
  fm <- binomial();fm$link <- "logit"
  roc_res <- data.frame(matrix(nrow=rep,ncol=9)) ; colnames(roc_res) <- c("AUC","HL")
  l <- nrow(data_old)-floor(0.7*nrow(data_old))
  old_prediction <- data.frame(matrix(nrow=l,ncol=rep)) ; new_prediction <- data.frame(matrix(nrow=l,ncol=rep)) ;actual_resp <- data.frame(matrix(nrow=l,ncol=rep))
  for(i in 1:rep){
    print(i)
    
    train_ind <- sample(1:nrow(data_old),size = floor(0.7*nrow(data_old)))
    test_ind <- setdiff(1:nrow(data_old),train_ind)
    train_data1 <- data_old[train_ind,] ; test_data1 <- data_old[test_ind,]
    train_data2 <- data_new[train_ind,] ; test_data2 <- data_new[test_ind,]
    outcome_test <- outcome[test_ind]
    model_o <- gam(s_o, data = train_data1, family = fm,method = "REML") ; model_n <- gam(s_n, data = train_data2, family = fm,method = "REML") 
    pred_o <- predict(model_o,newdata = test_data1,type="response") ; pred_n <- predict(model_n,newdata = test_data2,type="response")
    old_prediction[,i] <- pred_o ; new_prediction[,i] <- pred_n ; actual_resp[,i] <- outcome_test
    
    
  }
  nri_out <- NRI(old_prediction,new_prediction,actual_resp,cutoff)
  cfnri_out <- cfNRI(old_prediction,new_prediction,actual_resp,cutoff)
  idi_out <- IDI(old_prediction,new_prediction,actual_resp,cutoff)
  
  output_res <- as.data.frame(round(cbind(nri_out$NRIe,nri_out$NRIn,nri_out$NRI,cfnri_out$cfNRIe,cfnri_out$cfNRIn,cfnri_out$cfNRI,idi_out$IDIe,idi_out$IDIn,idi_out$IDI),3))
  ty <- c("e","n","")
  colnames(output_res) <- c(paste("NRI",ty,sep = ""),paste("cfNRI",ty,sep = ""),paste("IDI",ty,sep = ""))
  return(output_res)
  
}

#Plot funtions
plot_risk_1spline <- function(model,var,x_lab){
  model_data <- model$model ;  x_axis <- model_data[,which(colnames(model_data)==var)]; var_s <- paste("s(",var,")",sep="") ; 
  pred_terms <- predict(model,type="terms",se.fit = TRUE)  ; y_axis1 <- pred_terms$fit[,which(colnames(pred_terms$fit)==var_s)]
  y_axis <- exp(y_axis1)/(1+exp(y_axis1)) ; plot_data <- as.data.frame(cbind(x_axis,y_axis) ) ; colnames(plot_data) <- c("x_axis","y_axis")
  st_err1 <- pred_terms$se.fit[,which(colnames(pred_terms$se.fit)==var_s)] ;
  st_err_ul <- exp(y_axis1+1.96*st_err1)/(1+exp(y_axis1+1.96*st_err1)) ; st_err_ll <- exp(y_axis1-1.96*st_err1)/(1+exp(y_axis1-1.96*st_err1)) ; 
  plot_data$st_err_ul  <- st_err_ul ; plot_data$st_err_ll <- st_err_ll
  
  plot_data <- plot_data[order(plot_data$x_axis),] ; plot_data$group <- cut(plot_data$x_axis,100,label=FALSE)
  temp1 <- aggregate(plot_data$x_axis,list(plot_data$group),mean) ; temp2 <- aggregate(plot_data$y_axis,list(plot_data$group),mean)
  temp3 <- aggregate(plot_data$st_err_ul,list(plot_data$group),mean) ; temp4 <- aggregate(plot_data$st_err_ll,list(plot_data$group),mean)
  plot_data_r <- as.data.frame(cbind(temp1$x,temp2$x,temp3$x,temp4$x)) ; colnames(plot_data_r) <- c("x_axis","y_axis","st_err_ul","st_err_ll")
  
  plot(plot_data_r$x_axis,plot_data_r$y_axis,ylim=c(0,1),ylab="Predicted Risk",xlab=x_lab,type="l")
  polygon(c(plot_data_r$x_axis,rev(plot_data_r$x_axis)),c(plot_data_r$st_err_ul,rev(plot_data_r$st_err_ll)),
          border = FALSE,col="lightgrey")
  lines(plot_data_r$x_axis,plot_data_r$y_axis,lwd=2)
  
  sum_model <- summary(model) ; spline_val <- sum_model$s.table
  dof <- round(spline_val[which(names(spline_val[,1])==var_s),1],1) ; p_val <- round(spline_val[which(names(spline_val[,4])==var_s),4],3)
  
  legend("topright",legend=c(paste("DoF: ",dof,sep = ""),paste("p_value: ",p_val,sep = "")),cex=0.8)
  
}
plot_risk_2var <- function(model,var_list,seq_l,var_lab){
  if(length(var_list)>2)
    print("only first two variables considered")
  
  temp_data <- model$model ; test_data <- temp_data
  ind1 <- which(colnames(temp_data)==var_list[1]) ; ind2 <- which(colnames(temp_data)==var_list[2])
  var1_ll <- quantile(temp_data[,ind1],0.01,na.rm = TRUE) ; var1_ul <- quantile(temp_data[,ind1],0.99,na.rm = TRUE)
  var2_ll <- quantile(temp_data[,ind2],0.01,na.rm = TRUE) ; var2_ul <- quantile(temp_data[,ind2],0.99,na.rm = TRUE)
  var1_seq <- seq(var1_ll,var1_ul,length.out = seq_l[1]) ;  var2_seq <- seq(var2_ll,var2_ul,length.out = seq_l[2]) 
  rnd1 <- 0 ; rnd2 <- 0 ;
  if(diff(range(var1_seq))<15)
    rnd1 <- 1
  if(diff(range(var2_seq))<15)
    rnd2 <- 1
  var1_seq <- round(var1_seq,rnd1) ; var2_seq <- round(var2_seq,rnd2)
  
  test_plot <- data.frame(matrix(nrow=seq_l[1]*seq_l[2],ncol=3)) ; colnames(test_plot) <- c("x1_val","x2_val","risk") ; index <- 1
  for(i in 1:seq_l[1]){
    print(i)
    for(j in 1:seq_l[2]){
      test_data[,ind1] <- var1_seq[i] ; test_data[,ind2] <- var2_seq[j]
      pred <- predict.gam(model,test_data,type = "response")
      test_plot$x1_val[index] <- var1_seq[i] ; test_plot$x2_val[index] <- var2_seq[j]
      test_plot$risk[index] <- mean(pred,na.rm = TRUE)
      index <- index+1
    }
  }
  test_plot$Relative_risk <- test_plot$risk/min(test_plot$risk,na.rm = TRUE)
  ## plot the scatter plots
  ggplot(test_plot,aes(x1_val,x2_val)) + geom_tile(aes(fill=risk)) + scale_fill_gradient(low="green",high="red") + 
    labs(x=var_lab[1],y=var_lab[2],title="Relative Risk Plot " )
  ## plot the scatter plots
  ggplot(test_plot,aes(x1_val,x2_val)) + geom_tile(aes(fill=Relative_risk)) + scale_fill_gradient(low="green",high="red") + 
    labs(x=var_lab[1],y=var_lab[2],title="Relative Risk Plot " )
  return(test_plot)
}

plot_risk_cat <- function(outcome,pred,lim1,lim2){
  obser <- rep(0,times = length(outcome))
  obser[which(outcome==1)] <- 1 ; obser <- as.numeric(obser)
  score <- as.numeric(pred)
  temp_var <- rep(2,length(obser))
  temp_var[score<lim2] <- 1 ; temp_var[score<lim1] <- 0 
  temp_data <- as.data.frame(cbind(obser,temp_var)) ; colnames(temp_data) <- c("outcome","variable")
  s <- as.formula("outcome~variable") ;  fm<-binomial();  fm$link = "logit";
  temp_data$variable <- as.factor(temp_data$variable)
  mod <- glm(s,fm,temp_data) ; sum_mod <- summary(mod)
  yval <- round(c(1,exp(coef(mod))[2],exp(coef(mod))[3]),1)
  x_labs <- c("Low","Medium","High")
  se <- round(exp(confint.default(mod)),1) ; y_lim <- c(-5,(1+ceiling(max(se))))
  
  per_cat <- round(100*table(temp_var)/length(temp_var),0)
  abs_risk <- per_cat ; 
  abs_risk[1] <- round(100*length(which(temp_data$outcome==1&temp_data$variable==0))/length(which(temp_data$variable==0)),0)
  abs_risk[2] <- round(100*length(which(temp_data$outcome==1&temp_data$variable==1))/length(which(temp_data$variable==1)),0)
  abs_risk[3] <- round(100*length(which(temp_data$outcome==1&temp_data$variable==2))/length(which(temp_data$variable==2)),0)
  abs_risk_p <- paste("[",abs_risk,"%]",sep="")
  plot(c(1,2,3),yval,xlim = c(1,3.5),ylim=y_lim,xlab="Predicted Risk Category",
       ylab="Odds Ratio",xaxt = 'n',pch=18)
  lines(1:3,yval)  
  axis(1,at=c(1,2,3),labels = x_labs,0)
  pt_name <- c("1 (1 , 1)",paste(yval[2]," (",se[2,1]," , ",se[2,2],")",sep = ""),paste(yval[3]," (",se[3,1]," , ",se[3,2],")",sep = ""))
  text(c(1,2,3),c(1,yval[2:3]),pt_name,cex=0.8,pos=4)
  if(max(yval,na.rm = T)>80){text(c(1,2,3),c(-3,yval[2:3]-5),abs_risk_p,cex=0.85,pos=4)}else{
    text(c(1,2,3),c(-1,yval[2:3]-2.5),abs_risk_p,cex=0.85,pos=4)
  }
  
  lines(c(2,2),se[2,1:2],lwd = 2) ; lines(c(3,3),se[3,1:2],lwd=2)
  legend("topleft",legend=c(paste("Low (<",lim1,")",sep = ""),paste("Medium (>=",lim1," to <",lim2,")",sep=""),
                            paste("High (>=",lim2,")",sep="")),bty="n")
  legend("bottomright",legend=c("Odds Ratio (95% CI)","[Absolute Risk %]"),bty="n")
}

plot_roc_rev <- function(outcome, pred,cut1,cut2,heading){
  obser <- rep(0,times = length(outcome))
  obser[which(outcome==1)] <- 1 ; obser <- as.numeric(obser)
  score <- as.numeric(pred)
  #roc_area <- roc.area(obser,score)
  #roc.plot(obser,score,main=paste("ROC curve, AUC:",round(roc_area$A,digits=2),sep=""))
  prev <- round(sum(obser)/length(obser),digits=2)
  thres <- seq(0.01,max(score),length.out=100) ; thres <- thres[-c(99,100)]
  xval <- thres
  acc <- array(dim=length(thres))
  ppv <- array(dim=length(thres))
  npv <- array(dim=length(thres))
  sen <- array(dim=length(thres))
  spe <- array(dim=length(thres))
  yod <- array(dim=length(thres))
  for(l in 1:length(thres)){
    plotdata <- ROC_parameters(obser,score,thres[l])
    acc[l] <- round(plotdata$acc,3)
    ppv[l] <- round(plotdata$ppv,3)
    npv[l] <- round(plotdata$npv,3)
    sen[l] <- round(plotdata$sen,3)
    spe[l] <- round(plotdata$spe,3)
    yod[l] <- round(plotdata$yod,3)
  }
  
  cut1_ind <- which(abs(thres-cut1)==min(abs(thres-cut1))) ; cut2_ind <- which(abs(thres-cut2)==min(abs(thres-cut2)))
  plot(c(1,1-spe),c(1,sen),xlab="1-Specificity",ylab="Sensitivity",xlim=c(0,1),ylim=c(0,1),type="l",lwd=2)
  mtext(heading,side = 3,line = 1)
  x1 <- c(1-spe[cut1_ind],1-spe[cut2_ind]) ; y1 <- c(sen[cut1_ind],sen[cut2_ind])
  points(x1,y1,pch=15)
  cutoffs <- c(paste("Cutoff1 (",round(thres[cut1_ind],2),")",sep=""),paste("Cutoff2 (",round(thres[cut2_ind],2),")",sep=""))
  text(x1+0.01,y1-0.01,cutoffs,pos=4)
  auc <- round(roc.area(obser,score)$A,3)
  text(0.6,0.2,paste("AUC",auc),pos=4)
  
}

roc_parm_merge <- function(obser,pred,cut){
  result <- ROC_parameters(obser,pred,cut) ; 
  res <- as.data.frame(matrix(nrow=1,ncol=length(result)))
  res[1,1:ncol(res)] <- as.numeric(unlist(result))
  colnames(res) <- names(result)
  return(res)
}

create_table2 <- function(model){
  # Results for Table 2 (Odds ratio for the variables in the model)
  ods <- round(exp(coef(model)),2) ; odd_ci <- exp(confint.default(model,level=0.99)) ; ci_ll <- round(odd_ci[,1],2) ; ci_ul <- round(odd_ci[,2],2)
  ci <- paste("(",ci_ll," , ",ci_ul,")",sep="")       
  table2 <- cbind(ods,ci) ; colnames(table2) <- c("Odds_Ratio","Odds_Ratio_CI_99%")
  return(table2)
}
