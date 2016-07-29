# read all the required data files 
# raw data files are modified to create new variables  (based on various discussions)

#genpath <- "C:/Users/Swati/Documents/R/SEP" ### define the location of files 
genpath  <- "/home/rbhat/workspace/S3Lab_Projects/Deep-Medicine/RCodesforTesting"
filename <- file.path(genpath,"processeddata.csv")
data_raw <- read.csv(file=filename,header = TRUE)

filename <- file.path(genpath,"feature_list.csv")
features <- read.csv(file=filename,header = TRUE)

filename <- file.path(genpath,"feature_list_all.csv")
features_all <- read.csv(file=filename,header = TRUE)

t <- ifelse(data_raw$nsaids_adm==1&(data_raw$vanco_adm==1|data_raw$diuret_adm==1|data_raw$aminog_adm==1),2,
            ifelse(data_raw$nsaids_adm==1,1,0))



data_raw$nephtox_adm <- t 


# create Number of nephrotoxic medications
ind <- which(colnames(data_raw)%in%c("aminog_adm","diuret_adm","vanco_adm","ace_adm","nsaids_adm","inot_pres_adm"))
no_nephrotoxic_meds <- rowSums(data_raw[,ind],na.rm = T)
data_raw$no_nephrotoxic_meds <- no_nephrotoxic_meds

# grouping Urine Protein
t <- ifelse(data_raw$max_PROTUR_gr2==">=300",2,ifelse(data_raw$max_PROTUR_gr2=="TR-30-100",1,0))

# grouping urinal hemoglobin
t <- ifelse(data_raw$max_HGBUR_gr=="Large",2,ifelse(data_raw$max_HGBUR_gr=="Missing"|data_raw$max_HGBUR_gr=="NEGATIVE",0,1))
data_raw$max_HGBUR_gr <- as.factor(t)

# grouping urinal glucose
t <- ifelse(data_raw$max_GLUURN_gr=="Large",2,ifelse(data_raw$max_GLUURN_gr=="Missing"|data_raw$max_GLUURN_gr=="NEGATIVE",0,1))
data_raw$max_GLUURN_gr <- as.factor(t)

# grouping of No of complete blood count tests
t <- ifelse(data_raw$count_HGBn==0,0,ifelse(data_raw$count_HGBn==1,1,"2 or more"))
data_raw$count_HGBn <- t

