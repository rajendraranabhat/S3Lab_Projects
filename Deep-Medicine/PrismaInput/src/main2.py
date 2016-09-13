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
import zipcode_information as zz

#path = 'M:/IDEALIST/3 IDEALIST Data Core/2 Working Data/Creating Fake Stream Data/'
path ="/home/rbhat/workspace/S3Lab_Projects/Deep-Medicine/PrismaInput/"
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
            'Admission_Source',
            'Primary_Payer',
            'Admitting_Service',
            'Discharge_Service',
            'Admission_Source',
            'Admission_Date',
            'Discharge_Date',
            'Year_of_Discharge',
            'Icd_9_Proc_1',
            'Icd_9_Proc_2',
            'Days_from_Admission_for_Proc_1',
            'Admission_Type',
            'DX1','DX2','DX3','DX4','DX5','DX6','DX7','DX8','DX9','DX10','DX11','DX12','DX13','DX14','DX15','DX16',
            'Count_of_Diagnosis_Codes','DRG','CKD_corr','esrd_corr','eGFR_epi_new','ratio_firstCr_mdrd'
]

    df = pd.read_csv(path+'admission_data.csv',usecols=read_var)
    df['Admission_Date']= pd.to_datetime(df['Admission_Date'])

    #Getting Provider Information from ip.CSV
    print("Loading Provider Information...")
    provider = mp.get_provider_map(path)


    #Getting Lab results on admission day for each account
    print("Loading Lab Results for patients...")
    ll = pd.DataFrame(columns=['Account','Admission_Date'])
    ll['Account'] = df['Account']
    ll['Admission_Date'] = df['Admission_Date']
    lab_results= lc.load_labs_data(ll,path)

    #Getting medicine intake for patients on admisision day
    print("Loading Medicine Information for patients")
    med_results= md.load_meds_data(ll ,path)

    #Loading zip information
    print("Loading demographic data")
    zipdf  = pd.read_csv(path+'zip.csv')
    zipmap = pd.read_csv(path+'zip_to_zcta_2015.csv')
    print zipmap


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
    df['max_PROTUR_gr2']=np.nan
    df['max_HGBUR_gr']=np.nan
    df['max_GLUURN_gr']=np.nan
    df['count_HGBn']=np.nan
    df['count_PROTURn']=np.nan


#renaming existing columns
    df.rename(columns={'Account': 'acc'}, inplace=True)
    df.rename(columns={'Days_from_Admission_for_Proc_1': 'pr1_day'}, inplace=True)
    df.rename(columns={'Count_of_Diagnosis_Codes': 'NDX'}, inplace=True)
    df.rename(columns={'Zip': 'zip5'}, inplace=True)
    df.rename(columns={'Age': 'age'}, inplace=True)
    #temporary change
    df.rename(columns={'dx1': 'DX1'}, inplace=True)
    df.rename(columns={'dx2': 'DX2'}, inplace=True)
    df.rename(columns={'dx3': 'DX3'}, inplace=True)
    df.rename(columns={'dx4': 'DX4'}, inplace=True)
    df.rename(columns={'dx5': 'DX5'}, inplace=True)
    df.rename(columns={'dx6': 'DX6'}, inplace=True)
    df.rename(columns={'dx7': 'DX7'}, inplace=True)
    df.rename(columns={'dx8': 'DX8'}, inplace=True)
    df.rename(columns={'dx9': 'DX9'}, inplace=True)
    df.rename(columns={'dx10': 'DX10'}, inplace=True)
    df.rename(columns={'dx11': 'DX11'}, inplace=True)
    df.rename(columns={'dx12': 'DX12'}, inplace=True)
    df.rename(columns={'dx13': 'DX13'}, inplace=True)
    df.rename(columns={'dx14': 'DX14'}, inplace=True)
    df.rename(columns={'dx15': 'DX15'}, inplace=True)
    df.rename(columns={'dx16': 'DX16'}, inplace=True)

#Iterating over rows to standardize parameters
    print("Processing Data")

    for index, row in df.iterrows():
    #processing suf data
        print('Processing row '+ str(index) + '...')
        df.ix[index, 'race2']                      = sf.standardize_race(row['Race'])
        df.ix[index, 'pay_grp']                   = sf.standardize_pay_group(row['Primary_Payer'])
        df.ix[index, 'Admitting_type']            = sf.standardize_admitting_type(row['Admitting_Service'])
        df.ix[index, 'Admission_Source']          = sf.standardize_admission_source(row['Admission_Source'])
        df.ix[index, 'admit_day1']                = sf.day(row['Admission_Date'])
        df.ix[index, 'admit_mth']                 = sf.month(row['Admission_Date'])
        df.ix[index, 'Year_of_admission']         = sf.year(row['Admission_Date'])
        df.ix[index, 'weekend_adm']               = sf.isWeekend(df.ix[index, 'admit_day1'])
        df.ix[index, 'emergent']                  = sf.standardize_admission_type(row['Admission_Type'])
        df.ix[index, 'pr1c']                      = sf.standardize_proc_code(row['Icd_9_Proc_1'])
        df.ix[index, 'Count_of_Diagonosis_Codes'] = sf.standardize_proc_code(row['Icd_9_Proc_1'])
        df.ix[index, 'PEDS']                      = sf.mark_as_ped(str(row['Discharge_Service']),str(row['Admitting_Service']))
        df.ix[index, 'service1'] = sf.standardize_service(str(row['Admitting_Service']),str(row['Discharge_Service']),str(row['Icd_9_Proc_1']),str(row['Icd_9_Proc_2']))
    #Getting income and zip level information with race and zip

        zipinfo = zz.get_zip_Info(str(row['zip5']),str(row['Race']),zipdf,zipmap)
        df.ix[index, 'total']       = zipinfo['total']
        df.ix[index, 'rural']       = zipinfo['rural']
        df.ix[index, 'Med_inc']     = zipinfo['Med_inc']
        df.ix[index, 'prop_black']  = zipinfo['prop_black']
        df.ix[index, 'prop_hisp']   = zipinfo['prop_hisp']
        df.ix[index, 'Prop_pov']    = zipinfo['prop_pov']
        df.ix[index, 'zipdist2']    = zipinfo['zipdist2']

    #getting info from maps
        try:
            df.ix[index, 'attend_doc'] = provider[row['acc']]
        except ValueError:
            df.ix[index, 'attend_doc'] = "None"
        except KeyError:
            df.ix[index, 'attend_doc'] = "None"

    # cci calculation
        conditions = cc.CharlsonICD9CM([str(row['DX1']),  str(row['DX2']),  str(row['DX3']),  str(row['DX4']),  str(row['DX5']),  str(row['DX6']),
                                        str(row['DX7']),  str(row['DX8']),  str(row['DX9']),  str(row['DX10']), str(row['DX11']), str(row['DX12']),
                                        str(row['DX13']), str(row['DX14']), str(row['DX15'])])


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
        conditions2 = cc2.comorb2_condition([str(row['DX1'] ), str(row['DX2']), str(row['DX3']), str(row['DX4']), str(row['DX5']), str(row['DX6']),
                                              str(row['DX7']), str(row['DX8']), str(row['DX9']), str(row['DX10']), str(row['DX11']), str(row['DX12']),
                                              str(row['DX13']), str(row['DX14']), str(row['DX15'])] ,str(row['DRG']) )

        df.ix[index, 'VALVE']    = conditions2['VALVE']
        df.ix[index, 'HYPOTHY']  = conditions2['HYPOTHY']
        df.ix[index, 'COAG']     = conditions2['COAG']
        df.ix[index, 'OBESE']    = conditions2['OBESE']
        df.ix[index, 'WGHTLOSS'] = conditions2['WGHTLOSS']
        df.ix[index, 'LYTES']    = conditions2['LYTES']
        df.ix[index, 'anemia']   = conditions2['anemia']
        df.ix[index, 'alc_drug'] = conditions2['alc_drug']
        df.ix[index, 'DEPRESS']  = conditions2['DEPRESS']
        df.ix[index, 'HTN_C']    = conditions2['HTN_C']
        df.ix[index, 'PARA']     = conditions2['PARA']
        df.ix[index, 'NEURO']    = conditions2['NEURO']


    # adding information about medicaitons
        med = med_results[row['acc']]
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
        lab = lab_results[row['acc']]
        df.ix[index,'min_HGB']         = lab['min_HGB']
        df.ix[index,'max_PROTUR_gr2']  = lab['max_PROTUR_grp2']
        df.ix[index,'max_HGBUR_gr']    = lab['max_HGBUR_gr']
        df.ix[index,'max_GLUURN_gr']   = lab['max_GLUURN_gr']
        df.ix[index,'count_HGBn']      = lab['count_HGBn']
        df.ix[index,'count_PROTURn']   = lab['count_PROTURn']

    print(len(df))
    print(df[df['PEDS'] == 1])
    df = df[df['PEDS'] == 0]
    print(len(df))
#Dropping extraneous Columns
    df.drop(['Race','Primary_Payer','Admission_Date','Icd_9_Proc_1','Icd_9_Proc_2','Discharge_Service','DRG','PEDS'],axis=1,inplace=True)
    df.drop(['DX1','DX2','DX3','DX4','DX5','DX6','DX7','DX8','DX9','DX10','DX11','DX12','DX13','DX14','DX15','DX16'],axis=1,inplace=True)
    #df.drop(['dx1', 'dx2', 'dx3', 'dx4', 'dx5', 'dx6', 'dx7', 'dx8', 'dx9', 'dx10', 'dx11', 'dx12', 'dx13', 'dx14', 'dx15', 'dx16'],axis=1,inplace=True)

    df=df[['acc','age','Gender','race2','zip5','pay_grp','County','rural','total','Med_inc','prop_black','prop_hisp','Prop_pov','zipdist2','admit_day1','admit_mth',	'Year_of_admission',	'weekend_adm',	'attend_doc',	'Admission_Source',	'Admitting_Service',	'Admitting_type',	'emergent',	'pr1_day',	'service1',	'pr1c',	'cci',	'NDX',	'MDC',	'imi',	'ichf',	'ipvd',	'icvd',	'icpd',	'liverd',	'diabetes',	'icancer',	'imcancer',	'cancer',	'VALVE',	'HYPOTHY',	'COAG',	'OBESE',	'WGHTLOSS',	'LYTES',	'alc_drug','anemia','DEPRESS','HTN_C','PARA','NEURO','no_meds_on_adm','aminog_adm','bicarb_adm','diuret_adm','steroi_adm','vanco_adm','ace_adm','nsaids_adm','asa_adm','antiemetic_adm','betablockers_adm','statin_adm','inot_pres_adm','min_HGB','max_PROTUR_gr2','max_HGBUR_gr','max_GLUURN_gr','count_HGBn','count_PROTURn','CKD_corr','esrd_corr','eGFR_epi_new','ratio_firstCr_mdrd']]

    print("Processing of data complete.Writing to csv...")
    df.to_csv("processeddata.csv" ,sep=',',index = False)

    print("Writing to csv complete.Final File generated")
    print time.clock() - t0, "seconds process time"
    
    return df.to_json()



#preprocess()

json_message = preprocess()
print json_message

with open('prisma_input.json', 'w') as f:
    f.write(json_message)