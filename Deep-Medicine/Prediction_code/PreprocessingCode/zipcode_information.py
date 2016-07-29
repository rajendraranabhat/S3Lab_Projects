#Swati Tezcan Version
import re

def IsDigit(s):
  return re.search("[A-Za-z]", s) is None

def get_zip_Info(zip,race,zipdf,zipmap):
    if IsDigit(zip):
        if int(zip) not in zipdf.zipcode.values :
            if int(zip) in zipmap.ZIP.values :
                zcta_row = zipmap[zipmap['ZIP'] == int(zip)]
                zip = zcta_row['ZCTA'].values[0]
            else:
                zipInformation = {
                'rural': 'NA',
                'total': 'NA',
                'Med_inc':'NA',
                'prop_black': 'NA',
                'prop_hisp': 'NA',
                'prop_pov': 'NA',
                'zipdist2': 'NA'}
                return zipInformation


        zcta_row = zipdf[zipdf['zipcode'] == int(zip)]

        if(race == 'White'):
            Med_inc = zcta_row['med_white'] if zcta_row['med_white'].values[0] != '-' else zcta_row['median_income'].values[0]
        elif (race == 'Black'):
            Med_inc = zcta_row['med_black'] if zcta_row['med_black'].values[0] != '-' else zcta_row['median_income'].values[0]
        elif (race == 'Hispanic'):
            Med_inc = zcta_row['med_hispanic'] if zcta_row['med_hispanic'].values[0] != '-' else zcta_row['median_income'].values[0]
        else:
            Med_inc = zcta_row['median_income'].values[0]


        rural       = zcta_row['rural'].values[0]
        total       = zcta_row['total'].values[0]
        prop_black  = zcta_row['prop_black'].values[0]
        prop_hisp   = zcta_row['prop_hisp'].values[0]
        prop_pov    = zcta_row['prop_pov'].values[0]
        zipdist2    = zcta_row['distance_from_shands'].values[0]

        zipInformation = {
                'rural'     : rural,
                'total'     : total,
                'Med_inc'   : Med_inc,
                'prop_black': prop_black,
                'prop_hisp' : prop_hisp,
                'prop_pov'  : prop_pov,
                'zipdist2'  : zipdist2}
        return zipInformation
    else:
        zipInformation = {
            'rural': 'NA',
            'total': 'NA',
            'Med_inc': 'NA',
            'prop_black': 'NA',
            'prop_hisp': 'NA',
            'prop_pov': 'NA',
            'zipdist2': 'NA'}
        return zipInformation
