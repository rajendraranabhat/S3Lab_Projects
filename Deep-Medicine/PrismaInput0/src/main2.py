#Swati Tezcan Version
#import core libraries
import pandas as pd
import numpy as np
import time
import labConversion as lc

#import all modules
import sufConversion2 as sf
import CharlsonComorbidity as cc
import map_Provider as mp
import medConversion as md
import comorbidity_conditions2 as cc2

path_csv = "/home/rbhat/workspace/S3Lab_Projects/Deep-Medicine/PrismaInput/"

def preprocess():
    #read raw files ( not reading extraneous columns to avoid unneccesary loading time)
    print("Loading Data from SUF....")
    t0 = time.clock()
    read_var = ['Account',
            'Age',
            'Gender',
            'Zip',
            'County',
            'Race',
            'MDC',
            'Patient Disposition',
            'Admission_Source',
            'Primary_Payer',
            'Admitting_Service',
            'Admission_Source',
            'Admission_Date',
            'Discharge_Date',
            'Year_of_Discharge',
            'ICD_9_Proc_1',
            'Days_from_Admission_for_Proc_1',
            'Admission_Type',
            'DX1','DX2','DX3','DX4','DX5','DX6','DX7','DX8','DX9','DX10','DX11','DX12','DX13','DX14','DX15','DX16',
            'Count_of_Diagonosis_Codes',
            'VALVE' ,'HYPOTHY','COAG','OBESE','WGHTLOSS','LYTES','alc_drug','anemia' ,'DEPRESS' ,'HTN_C','ace_adm',
            'CKD_corr','esrd_corr','PARA','NEURO','eGFR_epi_new','ratio_firstCr_mdrd','BLDLOSS','ANEMDEF',
            'ALCOHOL','DRUG','mort_status_30d','cv_comp_new','MV_comp','ICU_comp','rural','total','Med_inc','prop_black','prop_hisp','Prop_pov','zipdist2','service1'
            ]

    df = pd.read_csv(path_csv+'fake_data_admission.csv',usecols=read_var,skipfooter=1)


    #Getting Provider Information from ip.CSV
    print("Loading Provider Information...")
    provider = mp.get_provider_map()


    #Getting Lab results on admission day for each account
    print("Loading Lab Results for patients...")
    ll = pd.DataFrame(columns=['Account','Admission_Date'])
    ll['Account'] = df['Account']
    ll['Admission_Date'] = df['Admission_Date']
    lab_results= lc.load_labs_data(ll)

    #Getting medicine intake for patients on admisision day
    print("Loading Medicine Information for patients")
    med_results= md.load_meds_data(ll)

    print("Finished Loading Data.")

    #start processing
    #creating new columns
    df['pay_grp'] = np.nan
    df['admitting_type'] = np.nan
    df['race2'] = np.nan
    df['imi'] = np.nan
    df['ichf'] = np.nan
    df['ipvd'] = np.nan
    df['icvd'] = np.nan
    df['liverd'] = np.nan
    df['icancer'] = np.nan
    df['diabetes'] = np.nan
    df['imcancer'] = np.nan
    df['attend_doc'] = np.nan
    df['min_HGB'] = np.nan
    df['max_PROTUR_grp2']=np.nan
    df['max_HGBUR_gr']=np.nan
    df['max_GLUURN_gr']=np.nan
    df['count_HGBn']=np.nan
    df['count_PROTURn']=np.nan

#renaming existing columns
    df.rename(columns={'Days_from_Admission_for_Proc_1': 'pr1_day'}, inplace=True)
    df.rename(columns={'Count_of_Diagonosis_Codes': 'NDX'}, inplace=True)
    df.rename(columns={'Zip': 'zip5'}, inplace=True)
    df.rename(columns={'Age': 'age'}, inplace=True)


#Iterating over rows to standardize parameters
    print("Processing Data")

    for index, row in df.iterrows():
    #processing suf data
        df.ix[index, 'race']                      = sf.standardize_race(row['Race'])
        df.ix[index, 'pay_grp']                   = sf.standardize_pay_group(row['Primary_Payer'])
        df.ix[index, 'Admitting_type']            = sf.standardize_admitting_type(row['Admitting_Service'])
        df.ix[index, 'admission_source']          = sf.standardize_admission_source(row['Admission_Source'])
        df.ix[index, 'admit_day1']                = sf.day(row['Admission_Date'])
        df.ix[index, 'admit_mth']                 = sf.month(row['Admission_Date'])
        df.ix[index, 'Year_of_admission']         = sf.year(row['Admission_Date'])
        df.ix[index, 'weekend_adm']               = sf.isWeekend(df.ix[index, 'admit_day1'])
        df.ix[index, 'emergent']                  = sf.year(row['Admission_Type'])
        df.ix[index, 'pr1c']                      = sf.standardize_proc_code(row['ICD_9_Proc_1'])
        df.ix[index, 'Count_of_Diagonosis_Codes'] = sf.standardize_proc_code(row['ICD_9_Proc_1'])

    #getting info from maps
        try:
            df.ix[index, 'attend_doc'] = provider[row['Account']]
        except ValueError:
            df.ix[index, 'attend_doc'] = "None"
        except KeyError:
            df.ix[index, 'attend_doc'] = "None"

    # cci calculation
        conditions = cc.CharlsonICD9CM([str(row['DX1']),  str(row['DX2']),  str(row['DX3']),  str(row['DX4']),  str(row['DX5']),  str(row['DX6']),
                                    str(row['DX7']),  str(row['DX8']),  str(row['DX9']),  str(row['DX10']), str(row['DX11']), str(row['DX12']),
                                    str(row['DX13']), str(row['DX14']), str(row['DX15']), str(row['DX16'])])


        df.ix[index, 'imi']      = conditions[0]
        df.ix[index, 'ichf']     = conditions[1]
        df.ix[index, 'ipvd']     = conditions[2]
        df.ix[index, 'icvd']     = conditions[3]
        df.ix[index, 'icpd']     = conditions[5]
        df.ix[index, 'icancer']  = conditions[13]
        df.ix[index, 'imcancer'] = conditions[15]
        df.ix[index, 'cci']      = conditions[17]
        df.ix[index, 'cancer']   = conditions[18]
        df.ix[index, 'liverd']   = conditions[19]
        df.ix[index, 'diabetes'] = conditions[20]

    # comorbidity Macro2  related information
        conditions = cc2.translate_condition([str(row['DX1']), str(row['DX2']), str(row['DX3']), str(row['DX4']), str(row['DX5']), str(row['DX6']),
                                          str(row['DX7']), str(row['DX8']), str(row['DX9']), str(row['DX10']), str(row['DX11']), str(row['DX12']),
                                          str(row['DX13']), str(row['DX14']), str(row['DX15']), str(row['DX16'])])




    # adding information about medicaitons
        med = med_results[row['Account']]
        df.ix[index, 'no_meds_on_adm']   = med['no_meds_on_adm']
        df.ix[index, 'aminog_adm']       = med['aminog_adm']
        df.ix[index, 'bicarb_adm']       = med['bicarb_adm']
        df.ix[index, 'diuret_adm']       = med['diuret_adm']
        df.ix[index, 'steroi_adm']       = med['steroi_adm']
        df.ix[index, 'vanco_adm']        = med['vanco_adm']
        df.ix[index, 'ace_adm']          = med['ace_adm']
        df.ix[index, 'nsaids_adm']       = med['nsaids_adm']
        df.ix[index, 'asa_adm']          = med['asa_adm']
        df.ix[index, 'antiemetic_adm']   = med['antiemetic_adm']
        df.ix[index, 'betablockers_adm'] = med['betablockers_adm']
        df.ix[index, 'statin_adm']       = med['statin_adm']
        df.ix[index, 'inot_pres_adm']    = med['inot_pres_adm']

    #adding lab information
        lab = lab_results[row['Account']]
        df.ix[index,'min_HGB']         = lab['min_HGB']
        df.ix[index,'max_PROTUR_gr2']  = lab['max_PROTUR_grp2']
        df.ix[index,'max_HGBUR_gr']    = lab['max_HGBUR_gr']
        df.ix[index,'max_GLUURN_gr']   = lab['max_GLUURN_gr']
        df.ix[index,'count_HGBn']      = lab['count_HGBn']
        df.ix[index,'count_PROTURn']   = lab['count_PROTURn']


#Dropping extraneous Columns
    df.drop(['Race','Primary_Payer','Admission_Date','ICD_9_Proc_1'],axis=1,inplace=True)
    df.drop(['DX1','DX2','DX3','DX4','DX5','DX6','DX7','DX8','DX9','DX10','DX11','DX12','DX13','DX14','DX15','DX16'],axis=1,inplace=True)

    print("Processing of data complete.Writing to csv...")
    df.to_csv("processeddata.csv" ,sep=',',index = False)

    print("Writing to csv complete.Final File generated")
    print time.clock() - t0, "seconds process time"
    
    #print df.to_json()
    return df.to_json()

preprocess()