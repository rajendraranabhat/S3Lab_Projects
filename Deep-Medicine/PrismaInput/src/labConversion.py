#Swati Tezcan Version
import datetime
import pandas as pd
import numpy as np
import re

def clean(result) :

    cleanedRes = re.sub(r'[;,^*@<]',r' ',result)
    cleanedRes = cleanedRes.strip()
    return cleanedRes

def load_labs_data(mf,path):
    read_var = ['acc', 'coll_date','TestCode','Result']
    df = pd.read_csv(path+'lab_data.csv', usecols=read_var,skipinitialspace=True)

    AccountId = []
    labs =[]
    for index, row in mf.iterrows():
        try:
            #match acc and admitdate for lab.Process only the labs from admission date
            lab_rec = df[df['acc'] == row['Account']]
            lab_rec['coll_date'] = pd.to_datetime(lab_rec['coll_date'])
            sel_lab_rec = lab_rec[lab_rec['coll_date'] == row['Admission_Date']]
            sel_lab_rec = sel_lab_rec[sel_lab_rec['Result'] != 'HIDE']
            sel_lab_rec = sel_lab_rec[sel_lab_rec['Result'].isnull() != True ]

            if len(sel_lab_rec)>0:
                for i, r in sel_lab_rec.iterrows():                 #Clean up before processing
                    sel_lab_rec.ix[i,'Result']=clean(r['Result'])
                lab = process_labs(sel_lab_rec)

            else:
                lab = {'min_HGB': 'Missing',
                       'max_PROTUR_grp2': 'Missing',
                       'max_HGBUR_gr': 'Missing',
                       'max_GLUURN_gr': 'Missing',
                       'count_HGBn': 'Missing',
                       'count_PROTURn': 'Missing'}
        except ValueError:
            #no match found labs are missing
            lab = {'min_HGB': 'Missing',
                   'max_PROTUR_grp2':'Missing',
                   'max_HGBUR_gr':'Missing',
                   'max_GLUURN_gr': 'Missing',
                   'count_HGBn': 'Missing',
                   'count_PROTURn': 'Missing'}
        AccountId.append(row['Account'])
        labs.append(lab)
    return (dict(zip(AccountId, labs)))

def process_labs (df):
     count_HGB = count_PROTURn = 0
     #Select HGB Records with valid numeric data and take the min HGB value
     HGB_rec= df[df['TestCode']=='HGB']
     min_HGB =  HGB_rec['Result'].min()
     count_HGB = len(HGB_rec)
     if(count_HGB==0):
         min_HGB ='0'

     #Select PROTUR Records ,First assign then ranks to get max_Protur value , later name them according to rank

     PROTUR_rec = df[df['TestCode']=='PROTUR']

     for index, row in PROTUR_rec.iterrows():

        if "NEG" in row['Result'] :
            PROTUR_rec.ix[index,'Result'] = 0
        elif "TR" in row['Result'] :
            PROTUR_rec.ix[index, 'Result'] = 1
        elif row['Result'] in ('U30'):
            PROTUR_rec.ix[index, 'Result'] = 2
        elif row['Result'] in ('U100') :
            PROTUR_rec.ix[index, 'Result'] = 3
        elif row['Result'] in ('U300','UE300') :
            PROTUR_rec.ix[index, 'Result'] = 4
        elif row['Result'] in ('300','>300' ,'600','>600') :
            PROTUR_rec.ix[index, 'Result']= 5
        else :
            PROTUR_rec.ix[index, 'Result'] = 6;

     max_PROTUR = PROTUR_rec['Result'].max()


     if max_PROTUR == 0:
         max_PROTUR = 'NEGATIVE'
     elif max_PROTUR in (1,2,3):
         max_PROTUR = 'TR-30-100'
     elif max_PROTUR in (4,5):
         max_PROTUR = '>=300'
     else :
         max_PROTUR = 'Missing'

     PROTUR_rec = PROTUR_rec[PROTUR_rec['Result'] != 'Missing']
     count_PROTURn = len(PROTUR_rec)

     #HGBUR

     HGBUR_rec = df[df['TestCode']== 'HGBUR']
     for index, row in HGBUR_rec.iterrows():
         if "NEG" in row['Result']:
             HGBUR_rec.ix[index, 'Result'] = 0
         elif "TR" in row['Result'] :
             HGBUR_rec.ix[index, 'Result'] = 1
         elif row['Result'] in ('SMALL'):
             HGBUR_rec.ix[index, 'Result'] = 2
         elif row['Result'] in ('MOD'):
             HGBUR_rec.ix[index, 'Result'] = 3
         elif row['Result'] in ('LARGE'):
             HGBUR_rec.ix[index, 'Result'] = 4
         else:
             HGBUR_rec.ix[index, 'Result'] = 5

     max_HGBUR = HGBUR_rec['Result'].max()

     if max_HGBUR == 0:
         max_HGBUR ='NEGATIVE'
     elif max_HGBUR == 1:
         max_HGBUR ='TR'
     elif max_HGBUR == 2:
         max_HGBUR = 'Small'
     elif max_HGBUR == 3:
         max_HGBUR = 'Moderate'
     elif max_HGBUR == 4:
         max_HGBUR = 'Large'
     else :
         max_HGBUR ='Missing'


     #Gluurn

     GLUURN_rec = df[df['TestCode']== 'GLUURN']
     for index, row in GLUURN_rec.iterrows():
         if "NEG" in row['Result']:
             GLUURN_rec.ix[index, 'Result'] = 0
         elif row['Result'] in ('70', '150', 'U250', 'U250' , '300'):
             GLUURN_rec.ix[index,'Result'] = 1
         elif row['Result'] in ('U500','500'):
             GLUURN_rec.ix[index,'Result'] = 2
         elif row['Result'] in ('U1000','1000'):
             GLUURN_rec.ix[index,'Result'] = 3
         elif "LARGE" in row['Result'] :
             GLUURN_rec.ix[index,'Result'] = 4
         else:
             row['Result'] = 5

     max_GLUURN = GLUURN_rec['Result'].max()
     if max_GLUURN == 0:
         max_GLUURN = 'NEGATIVE'
     elif max_GLUURN == 1:
         max_GLUURN = 'Small'
     elif max_GLUURN == 2:
         max_GLUURN = 'Moderate'
     elif max_GLUURN == 3:
         max_GLUURN = 'Large'
     else:
         max_GLUURN = 'Missing'

     lab ={'min_HGB': min_HGB ,
           'max_PROTUR_grp2':max_PROTUR,
           'max_HGBUR_gr':max_HGBUR,
           'max_GLUURN_gr': max_GLUURN,
           'count_HGBn':count_HGB,
           'count_PROTURn':count_PROTURn}


     return lab