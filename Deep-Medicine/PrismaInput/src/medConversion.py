#Swati Tezcan Version

import pandas as pd
import numpy as np
import re

def load_meds_data(mf,path):
    df = pd.read_csv(path+'med_data.csv', skipinitialspace=True)
    AccountId = []
    meds =[]
    column_headers = list(df)

    #Not sure if file recived will have categories already assigned / Writing the code just in case category is missing
    if('Category' in column_headers):
        category_value_required =0
    else :
        category_value_required = 1
        df['Category']=np.nan

    for index, row in mf.iterrows():
        try:
            #match account and admit date for meds.Process only the meds from admission date
            med_rec = df[df['acc'] == row['Account']]
            med_rec['Service_Date'] = pd.to_datetime(med_rec['Service_Date'])
            sel_med_rec = med_rec[med_rec['Service_Date'] == row['Admission_Date']]
            sel_med_rec = sel_med_rec[sel_med_rec['Service_Date'].isnull() != True]

            if (len(sel_med_rec )> 0):
                # Make sure Categories are assigned
                for i, r in sel_med_rec.iterrows():
                    if(r['Category'] == 'nan'):

                        sel_med_rec.ix[i, 'Category'] = getCategory(r['Drug_Name'])

                #Process the Records
                med = process_meds(sel_med_rec)
            else:
                med = { 'no_meds_on_adm': 0,
                        'aminog_adm': 0,
                        'bicarb_adm': 0,
                        'diuret_adm': 0,
                        'steroi_adm': 0,
                        'vanco_adm': 0,
                        'ace_adm': 0,
                        'nsaids_adm': 0,
                        'asa_adm': 0,
                        'antiemetic_adm': 0,
                        'betablockers_adm': 0,
                        'statin_adm': 0,
                        'inot_pres_adm': 0}

        except ValueError:
            med = { 'no_meds_on_adm':0,
                    'aminog_adm':0,
                    'bicarb_adm':0,
                    'diuret_adm':0,
                    'steroi_adm':0,
                    'vanco_adm':0,
                    'ace_adm':0,
                    'nsaids_adm':0,
                    'asa_adm':0,
                    'antiemetic_adm':0,
                    'betablockers_adm':0,
                    'statin_adm':0,
                    'inot_pres_adm':0 }

        AccountId.append(row['Account'])
        meds.append(med)
    return (dict(zip(AccountId, meds)))

def process_meds(df):

    sel_df = df[df.Category.notnull()]

    if(len(sel_df) == 0):
        med = {'no_meds_on_adm': 0,
               'aminog_adm': 0,
               'bicarb_adm': 0,
               'diuret_adm': 0,
               'steroi_adm': 0,
               'vanco_adm': 0,
               'ace_adm': 0,
               'nsaids_adm': 0,
               'asa_adm': 0,
               'antiemetic_adm': 0,
               'betablockers_adm': 0,
               'statin_adm': 0,
               'inot_pres_adm': 0}
    else :
        #We dont need them all , but putting up the code for all just in case required for future
        med_lookup = {  'abelce': 0,'aminog':0,'bicarb':0,'cosynt':0,'ddavp':0,'diuret':0,'epi':0,'epo':0,'florin':0,'midodr':0,'neo':0,'norepi':0,'septra':0,
                        'steroi':0,'vanco':0,'vaso':0,'viral':0,'ace':0,'ht_sod':0,'iron':0,'nsaids':0,'asa':0,'ampho':0,'dobuta':0,'f7':0,'dopami':0,'milrin':0,
                        'contra':0,'nesiri':0,'viagra':0,'isopro':0,'ephedr':0, 'antiemetic':0,'betablockers':0,'statin':0}

        no_meds_on_adm = 0
        grouped = sel_df.groupby('Category')
        for name, group in grouped :
            total = group['Quantity'].sum()
            no_meds_on_adm += total
            if total>0 :
                med_lookup[name] = 1

        aminog_adm = 1 if med_lookup['aminog'] == 1  else 0
        bicarb_adm = 1 if med_lookup['bicarb'] == 1  else 0
        diuret_adm = 1 if med_lookup['diuret'] == 1  else 0
        epi_adm    = 1 if med_lookup['epi']    == 1  else 0
        neo_adm    = 1 if med_lookup['neo']    == 1  else 0
        norepi_adm = 1 if med_lookup['norepi'] == 1  else 0
        steroi_adm = 1 if med_lookup['steroi'] == 1  else 0
        vanco_adm  = 1 if med_lookup['vanco']  == 1  else 0
        vaso_adm   = 1 if med_lookup['vaso']   == 1  else 0
        ace_adm    = 1 if med_lookup['ace']    == 1  else 0
        nsaids_adm = 1 if med_lookup['nsaids'] == 1  else 0
        asa_adm    = 1 if med_lookup['asa']    == 1  else 0
        dobuta_adm = 1 if med_lookup['dobuta'] == 1  else 0
        dopami_adm = 1 if med_lookup['dopami'] == 1  else 0
        milrin_adm = 1 if med_lookup['milrin'] == 1  else 0
        ephedr_adm = 1 if med_lookup['ephedr'] == 1  else 0

        #ampho_adm  = 1 if med_lookup['ampho']  == 1  else 0
        #ht_sod_adm = 1 if med_lookup['ht_sod'] == 1  else 0
        #iron_adm   = 1 if med_lookup['iron']   == 1  else 0
        #abelce_adm = 1 if med_lookup['abelce'] == 1  else 0
        #cosynt_adm = 1 if med_lookup['cosynt'] == 1  else 0
        #ddavp_adm = 1 if med_lookup['ddavp'] == 1  else 0
        #epo_adm    = 1 if med_lookup['epo']    == 1  else 0
        #florin_adm = 1 if med_lookup['florin'] == 1  else 0
        #midodr_adm = 1 if med_lookup['midodr'] == 1  else 0
        #septra_adm = 1 if med_lookup['septra'] == 1  else 0
        #viral_adm  = 1 if med_lookup['viral']  == 1  else 0
        #f7_adm     = 1 if med_lookup['f7']     == 1  else 0
        #contra_adm = 1 if med_lookup['contra'] == 1  else 0
        #nesiri_adm = 1 if med_lookup['nesiri'] == 1  else 0
        #viagra_adm = 1 if med_lookup['viagra'] == 1  else 0
        #isopro_adm = 1 if med_lookup['isopro'] == 1  else 0

        antiemetic_adm   = 1 if med_lookup['antiemetic']   == 1  else 0
        betablockers_adm = 1 if med_lookup['betablockers'] == 1  else 0
        statin_adm       = 1 if med_lookup['statin']       ==1  else 0

        #define pressors
        pressor_adm = 0;
        inotrope_adm = 0;

        p_adm = neo_adm + epi_adm + dopami_adm + ephedr_adm + norepi_adm+ vaso_adm
        if p_adm > 0: pressor_adm = 1
        ino_adm = dobuta_adm + milrin_adm
        if ino_adm > 0 : inotrope_adm=1

        if pressor_adm == 1 or inotrope_adm ==1 :
            inot_pres_adm=1
        else :
            inot_pres_adm=0

        med = {'no_meds_on_adm': no_meds_on_adm,
                'aminog_adm': aminog_adm,
                'bicarb_adm': bicarb_adm,
                'diuret_adm': diuret_adm,
                'steroi_adm': steroi_adm,
                'vanco_adm': vanco_adm,
                'ace_adm': ace_adm,
                'nsaids_adm': nsaids_adm,
                'asa_adm': asa_adm,
                'antiemetic_adm': antiemetic_adm,
                'betablockers_adm': betablockers_adm,
                'statin_adm': statin_adm,
                'inot_pres_adm': inot_pres_adm}

    return med

def getCategory(drug_name):

    if drug_name == 'ACEBUTOLOL TAB 200M' :
        category = 'betablockers'
        return category
    if drug_name == 'APREPITANT CAP 125M' :
        category = 'antiemetic'
        return category
    if drug_name == 'APREPITANT CAP 80MG' :
        category = 'antiemetic'
        return category
    if drug_name == 'ATENOLOL LIQ 2MG/ML' :
        category = 'betablockers'
        return category
    if drug_name == 'ATENOLOL TAB 100MG'  :
        category = 'betablockers'
        return category
    if drug_name == 'ATENOLOL TAB 12.5MG' :
        category = 'betablockers'
        return category
    if drug_name == 'ATENOLOL TAB 25MG'   :
        category = 'betablockers'
        return category
    if drug_name == 'ATENOLOL TAB 50MG'   :
        category = 'betablockers'
        return category
    if drug_name == 'ATORVASTATIN TAB 10' :
        category = 'statin'
        return category
    if drug_name == 'ATORVASTATIN TAB 20' :
        category = 'statin'
        return category
    if drug_name == 'ATORVASTATIN TAB 40' :
        category = 'statin'
        return category
    if drug_name == 'ATORVASTATIN TAB 80' :
        category = 'statin'
        return category
    if drug_name == 'BETAXOLOL 0.25% OPS' :
        category = 'betablockers'
        return category
    if drug_name == 'BETAXOLOL 0.5% OPSO' :
        category = 'betablockers'
        return category
    if drug_name == 'BETAXOLOL TAB 10MG'  :
        category = 'betablockers'
        return category
    if drug_name == 'BISOPROLOL TAB 10MG' :
        category = 'betablockers'
        return category
    if drug_name == 'BISOPROLOL TAB 2.5M' :
        category = 'betablockers'
        return category
    if drug_name == 'BISOPROLOL TAB 5MG'  :
        category = 'betablockers'
        return category
    if drug_name == 'CAL CHLORIDE 4 GM/5' :
        category = 'cvvh'
        return category
    if drug_name == 'CARVEDILOL LIQD 1.6' :
        category = 'betablockers'
        return category
    if drug_name == 'CARVEDILOL TAB 12.5' :
        category = 'betablockers'
    	return category
    if drug_name == 'CARVEDILOL TAB 25MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'CARVEDILOL TAB 3.12' :
        category = 'betablockers'
    if drug_name == 'CARVEDILOL TAB 6.25' :
        category = 'betablockers'
    	return category
    if drug_name == 'CHLORPROMAZINE INJ'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'CHLORPROMAZINE SUPP' :
        category = 'antiemetic'
    	return category
    if drug_name == 'CHLORPROMAZINE TAB'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'DEXAMETHASONE INJ 2' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DEXAMETHASONE INJ 4' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DEXAMETHASONE LIQ 0' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DEXAMETHASONE LIQ 1' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DEXAMETHASONE OP 0.' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DEXAMETHASONE OPH I' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DEXAMETHASONE TAB 0' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DEXAMETHASONE TAB 1' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DEXAMETHASONE TAB 4' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DIPHENHYDRAMINE CAP' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DIPHENHYDRAMINE INJ' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DIPHENHYDRAMINE LIQ' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DIPHENHYDRAMINE2-0.' :
        category = 'antiemetic'
    	return category
    if drug_name == 'DROPERIDOL INJ 5MG'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'ESMOLOL INJ 100MG V' :
        category = 'betablockers'
    	return category
    if drug_name == 'ESMOLOL INJ 20 MG/M' :
        category = 'betablockers'
    	return category
    if drug_name == 'ESMOLOL INJ 2GM/100' :
        category = 'betablockers'
    	return category
    if drug_name == 'ESMOLOL SYRG 100 MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'FLUMAZENIL INJ 0.5'  :
        category = 'flumazenil'
    	return category
    if drug_name =='FLUMAZENIL INJ 1MG'   :
        category = 'flumazenil'
    	return category
    if drug_name == 'FLUVASTATIN CAP 20M' :
        category = 'statin'
    	return category
    if drug_name == 'FLUVASTATIN CAP 40M' :
        category = 'statin'
    	return category
    if drug_name == 'GRANISETRON INJ 100' :
        category = 'antiemetic'
    	return category
    if drug_name == 'GRANISETRON TAB 1MG' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HALOPERIDOL DEC INJ' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HALOPERIDOL INJ 50M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HALOPERIDOL INJ 5MG' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HALOPERIDOL LIQ 2MG' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HALOPERIDOL TAB 0.2' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HALOPERIDOL TAB 0.5' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HALOPERIDOL TAB 10M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HALOPERIDOL TAB 1MG' :
        category = 'antiemetic'
    	return category
    if drug_name =='HALOPERIDOL TAB 2MG'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'HALOPERIDOL TAB 5MG' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HYDROXYZINE HCL LIQ' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HYDROXYZINE INJ 100' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HYDROXYZINE INJ 25M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HYDROXYZINE INJ 50M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HYDROXYZINE TAB 10M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HYDROXYZINE TAB 25M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HYDROXYZINE TAB 50M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'HYDROXYZINE TAB 5MG' :
        category = 'antiemetic'
    	return category
    if drug_name == 'LABETALOL INJ 100MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'LABETALOL INJ 200MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'LABETALOL INJ 20MG/' :
        category = 'betablockers'
    	return category
    if drug_name == 'LABETALOL INJ 5MG/M' :
        category = 'betablockers'
    	return category
    if drug_name == 'LABETALOL LIQ 10MG/' :
        category = 'betablockers'
    	return category
    if drug_name == 'LABETALOL LIQD 20 M' :
        category = 'betablockers'
    	return category
    if drug_name == 'LABETALOL TAB 100MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'LABETALOL TAB 150MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'LABETALOL TAB 200MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'LABETALOL TAB 300MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'LABETALOL TAB 50MG'  :
        category = 'betablockers'
    	return category
    if drug_name == 'LEVOBUNOLOL 0.5% OP' :
        category = 'betablockers'
    	return category
    if drug_name == 'LEVOBUNOLOL OP 0.25' :
        category = 'betablockers'
    	return category
    if drug_name == 'LEVOBUNOLOL OP 0.5%' :
        category = 'betablockers'
    	return category
    if drug_name == 'LORAZEPAM INJ 2MG S' :
        category = 'antiemetic'
    	return category
    if drug_name == 'LORAZEPAM INJ 2MG/M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'LORAZEPAM INJ 4MG/M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'LORAZEPAM LIQ 1MG S' :
        category = 'antiemetic'
    	return category
    if drug_name == 'LORAZEPAM TAB 1MG'   :
        category = 'antiemetic'
    	return category
    if drug_name == 'LORAZEPAM TAB 500MC' :
        category = 'antiemetic'
    	return category
    if drug_name == 'LOVASTATIN TAB 10MG' :
        category = 'statin'
    	return category
    if drug_name == 'LOVASTATIN TAB 20MG' :
        category = 'statin'
    	return category
    if drug_name == 'MECLIZINE TAB 12.5M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'MECLIZINE TAB 25MG'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'METOCLOPRAMIDE INJ'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'METOCLOPRAMIDE LIQ'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'METOCLOPRAMIDE TAB'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'METOPROLOL 24HR TAB' :
        category = 'betablockers'
    	return category
    if drug_name == 'METOPROLOL INJ 1MG/' :
        category = 'betablockers'
    	return category
    if drug_name == 'METOPROLOL INJ 5MG'  :
        category = 'betablockers'
    	return category
    if drug_name == 'METOPROLOL LIQ 25 M' :
        category = 'betablockers'
    	return category
    if drug_name == 'METOPROLOL LIQ 50MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'METOPROLOL LIQD 10M' :
        category = 'betablockers'
    	return category
    if drug_name == 'METOPROLOL TAB 100M' :
        category = 'betablockers'
    	return category
    if drug_name == 'METOPROLOL TAB 12.5' :
        category = 'betablockers'
    	return category
    if drug_name == 'METOPROLOL TAB 25MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'METOPROLOL TAB 50MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'MIDAZOLAM 100MG/100' :
        category = 'antiemetic'
    	return category
    if drug_name == 'MIDAZOLAM INJ 2MG V' :
        category = 'antiemetic'
    	return category
    if drug_name == 'MIDAZOLAM INJ 5MG/1' :
        category = 'antiemetic'
    	return category
    if drug_name == 'MIDAZOLAM INJ 5MG/5' :
        category = 'antiemetic'
    	return category
    if drug_name == 'MIDAZOLAM INJ 5MG/M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'MIRTAZAPINE SOLTAB'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'MIRTAZAPINE TAB 15M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'MIRTAZAPINE TAB 30M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'MIRTAZAPINE TAB 7.5' :
        category = 'antiemetic'
    	return category
    if drug_name == 'NADOLOL TAB 20MG'    :
        category = 'betablockers'
    	return category
    if drug_name == 'NADOLOL TAB 40MG'    :
        category = 'betablockers'
    	return category
    if drug_name == 'NALOXONE INJ 0.4MG'  :
        category = 'naloxone'
    	return category
    if drug_name =='NALOXONE INJ 0.4MG/'  :
        category = 'naloxone'
    	return category
    if drug_name == 'NALOXONE INJ 4MG VL' :
        category = 'naloxone'
    	return category
    if drug_name == 'NALOXONE LIQD 0.4MG' :
        category = 'naloxone'
    	return category
    if drug_name == 'ONDANSETRON HCL TAB' :
        category = 'antiemetic'
    	return category
    if drug_name == 'ONDANSETRON INJ 0.5' :
        category = 'antiemetic'
    	return category
    if drug_name == 'ONDANSETRON INJ 2MG' :
        category = 'antiemetic'
    	return category
    if drug_name == 'ONDANSETRON INJ 4MG' :
        category = 'antiemetic'
    	return category
    if drug_name == 'ONDANSETRON LIQ 0.8' :
        category = 'antiemetic'
    	return category
    if drug_name == 'ONDANSETRON ODT TAB' :
        category = 'antiemetic'
    	return category
    if drug_name == 'ONDANSETRON TAB 4MG' :
        category = 'antiemetic'
    	return category
    if drug_name == 'ONDANSETRON TAB 8MG' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PINDOLOL TAB 10MG'   :
        category = 'betablockers'
    	return category
    if drug_name == 'PINDOLOL TAB 2.5MG'  :
        category = 'betablockers'
    	return category
    if drug_name == 'PINDOLOL TAB 5MG'    :
        category = 'betablockers'
    	return category
    if drug_name == 'POT CHLORIDE 40MEQ/' :
        category = 'cvvh'
    	return category
    if drug_name == 'PRAVASTATIN TAB 10M' :
        category = 'statin'
    	return category
    if drug_name == 'PRAVASTATIN TAB 20M' :
        category = 'statin'
    	return category
    if drug_name == 'PRAVASTATIN TAB 40M' :
        category = 'statin'
    	return category
    if drug_name == 'PROCHLORPERAZINE IN' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROCHLORPERAZINE SU' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROCHLORPERAZINE TA' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROMETHAZINE INJ 25' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROMETHAZINE INJ 50' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROMETHAZINE LIQ 1.' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROMETHAZINE SUPP 1' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROMETHAZINE SUPP 2' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROMETHAZINE TAB 12' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROMETHAZINE TAB 25' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROMETHAZINE TAB 6.' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROPOFOL INJ 10MG/M' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROPOFOL INJ 1GM/10' :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROPOFOL INJ 200MG'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROPOFOL INJ 500MG'  :
        category = 'antiemetic'
    	return category
    if drug_name == 'PROPRANOLOL INJ 1MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'PROPRANOLOL LIQ 4MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'PROPRANOLOL TAB 10M' :
        category = 'betablockers'
    	return category
    if drug_name == 'PROPRANOLOL TAB 20M' :
        category = 'betablockers'
    	return category
    if drug_name == 'PROPRANOLOL TAB 40M' :
        category = 'betablockers'
    	return category
    if drug_name == 'PROPRANOLOL TAB 5MG' :
        category = 'betablockers'
    	return category
    if drug_name == 'PROPRANOLOL TAB 80M' :
        category = 'betablockers'
    	return category
    if drug_name == 'ROSUVASTATIN TAB 10' :
        category = 'statin'
    	return category
    if drug_name == 'ROSUVASTATIN TAB 20' :
        category = 'statin'
    	return category
    if drug_name == 'SCOPOLAMINE INJ 0.4' :
        category = 'antiemetic'
    	return category
    if drug_name == 'SCOPOLAMINE OP 0.25' :
        category = 'antiemetic'
    	return category
    if drug_name == 'SCOPOLAMINE PATCH 1' :
        category = 'antiemetic'
    	return category
    if drug_name == 'SIMVASTATIN TAB 10M' :
        category = 'statin'
    	return category
    if drug_name == 'SIMVASTATIN TAB 20M' :
        category = 'statin'
    	return category
    if drug_name == 'SIMVASTATIN TAB 40M' :
        category = 'statin'
    	return category
    if drug_name == 'SIMVASTATIN TAB 5MG' :
        category = 'statin'
    	return category
    if drug_name == 'SOTALOL LIQD 5MG/ML' :
        category = 'betablockers'
    	return category
    if drug_name == 'SOTALOL TAB 120MG'   :
        category = 'betablockers'
    	return category
    if drug_name == 'SOTALOL TAB 240MG'   :
        category = 'betablockers'
    	return category
    if drug_name == 'SOTALOL TAB 40MG'    :
        category = 'betablockers'
    	return category
    if drug_name == 'SOTALOL TAB 60MG'    :
        category = 'betablockers'
    	return category
    if drug_name == 'SOTALOL TAB 80MG'    :
        category = 'betablockers'
    	return category
    if drug_name == 'TIMOLOL OP 0.25% 10' :
        category = 'betablockers'
    	return category
    if drug_name == 'TIMOLOL OP 0.25% 2.' :
        category = 'betablockers'
    	return category
    if drug_name == 'TIMOLOL OP 0.25% 5M' :
        category = 'betablockers'
    	return category
    if drug_name == 'TIMOLOL OP 0.5% 10M' :
        category = 'betablockers'
    	return category
    if drug_name == 'TIMOLOL OP 0.5% 2.5' :
        category = 'betablockers'
    	return category
    if drug_name == 'TIMOLOL OP 0.5% 5ML' :
        category = 'betablockers'
    	return category
    if drug_name == 'TRIMETHOBENZAMIDE C' :
        category = 'antiemetic'
    	return category
    if drug_name == 'TRIMETHOBENZAMIDE S' :
        category = 'antiemetic'
        return category

