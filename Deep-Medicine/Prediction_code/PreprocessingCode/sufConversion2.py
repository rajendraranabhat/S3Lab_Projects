#Swati Tezcan Version
from datetime import datetime


#Race Conversion function
def standardize_race(race):

        if race in ['AMERICAN INDIAN','OTHER','UNKNOWN','ASIAN']:
            return 'Other'
        elif race  == 'BLACK':
            return 'AA'
        elif race == 'HISPANIC' :
            return 'Hispanic'
        elif race == 'WHITE/CAUCASIAN':
            return 'White'
        else:
            return 'Missing'

#pay group conversion function

def standardize_pay_group(primary_payer):

        if primary_payer in ['MEDICARE' ,'MANAGED CARE - MCARE']:
            return 1
        elif primary_payer in ['MANAGED CARE - MCAID' ,'MEDICAID' ,'C. M. S.' ,'COUNTY PGMS' ,'FEDERAL PGMS' ,'STATE PGMS']:
            return 2
        elif primary_payer in ['MANAGED CARE', 'CHAMPUS' ,'COMMERCIAL' ,'WORKERS COMP'] :
            return 3
        elif primary_payer in  ['OTHER SPONSORSHIP','SELF PAY / PENDING']:
            return 4

def standardize_admitting_type(admitting_service):
        if admitting_service in ['Adult Cardiology Teaching' ,'Adult Electrophysiology Cardio' ,'Adult Heart Failure/Transplant','Adult Hospitalist Medicine','Adult Intervention Cardiology','Anesthesiology' ,'Internal Medicine' ,'Medicine Gastroenterology', 'Medicine Hematology/Oncology','Neurology' ,'Psychiatry' ,'Radiation Oncology']:
            return 'medicine'
        else :
            return 'surgery'

def standardize_admission_source(admission_source):
        if admission_source in ['TRANS-ANOTHER INSTIT', 'TRANS-CORRECTIONAL I' ,'TRANS-OTHER FACILITY', 'TRANS-SHORT TERM GEN', 'TRANSFER FROM SHANDS','TRANSFER FROM VISTA'] or "TRANS-" in admission_source :
            return 'transfer'
        elif admission_source  in ['OUTPATIENT CLINIC' ,'ROUTINE ADMISSION(SC', 'ROUTINE ADMISSION(UN', 'OP SERVICE', 'FAMILY PHYSICIAN REF' ,'HOME CARE SERVICE RE' ]:
            return 'outpatient'
        elif admission_source == 'EMERGENCY OP UNIT' :
            return 'ER'
        elif admission_source == 'Urgent':
            return 'Emergency'


def standardize_admission_type(admission_type):
    if admission_type == 'Emergency':
        return 1
    elif admission_type == 'Routine Elective':
        return 0

def day(date):
    try:
        date_object = date
        days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dayNumber=date_object.weekday()
        return days[dayNumber]
    except ValueError:
        return "Unknown"

def month(date):
    try:
        date_object = date
        months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","n/a"]
        month= date_object.month
        return month
    except ValueError:
        return "Unknown"


def year(date):
    try:
        date_object = date
        year=date_object.year
        return year
    except ValueError:
        return 0

def isWeekend(day):
    try:
        if day in ['Saturday','Sunday']:
            return 1
        else:
            return 0
    except ValueError:
        return "Unknown"

def standardize_proc_code(icdcode):
    icdcode1 = 'PR'+str(icdcode)
    return icdcode1


def standardize_service(Admitting_Service,Discharge_Service ,pr1,pr2):
    if Admitting_Service in (   'Surgery, Cardiovas/Thoracic' 'Thoracic/Cardiovascular Surger') or Discharge_Service in (
                                'Surgery, Cardiovas/Thoracic' 'Thoracic/Cardiovascular Surger'):
        service = 'CT_Surgery'
    elif Admitting_Service in ( 'Surgery, General/G.I.' 'Pancreas & Biliary Surgery' 'Minimally Invasive Surgery') or Discharge_Service in (
                                'Surgery, General/G.I.' 'Pancreas & Biliary Surgery' 'Minimally Invasive Surgery'):
        service = 'General_GI'
    elif Admitting_Service in ( 'Surgery, General/Oncology' 'Breast, Melanoma, Sarcoma, End') or Discharge_Service in (
                                'Surgery, General/Oncology' 'Breast, Melanoma, Sarcoma, End'):
        service = 'General_Oncology'
    elif Admitting_Service in ( 'Surgery, General/Colo-Rectal' 'Colorectal Surgery') or Discharge_Service in (
                                'Surgery, General/Colo-Rectal' 'Colorectal Surgery'):
        service = 'General_Colorectal';
    elif Admitting_Service in ( 'Surgery, Plastic/Reconst' "Plastic & Reconstructive Surge") or Discharge_Service in (
                                'Surgery, Plastic/Reconst' "Plastic & Reconstructive Surge"):
        service = 'Plastic';
    elif Admitting_Service in ( 'Surgery, Transplantation' 'Transplant Surgery') or Discharge_Service in (
                                'Surgery, Transplantation' 'Transplant Surgery'):
        service = 'Transplantation';
    elif Admitting_Service in ( 'Surgery, Vascular' 'Vascular Surgery') or Discharge_Service in (
                                'Surgery, Vascular' 'Vascular Surgery'):
        service = 'Vascular';
    elif Admitting_Service in ( 'Trauma - Acute Care Surgery') or Discharge_Service in (
                                'Trauma - Acute Care Surgery'):
        service = 'Trauma'
    elif Admitting_Service in ( 'Urology') or Discharge_Service in ( 'Urology'):
        service = 'Urology'
    elif Admitting_Service in ( 'Gynecology' 'Obstetrics') or Discharge_Service in (
                                'Gynecology' 'Obstetrics'):
        service = 'OB_GYN'
    elif Admitting_Service in ( 'Burn/Wound Surgery' 'Burn Surgery') or Discharge_Service in (
                                'Burn/Wound Surgery' 'Burn Surgery'):
        service = 'Burn'
    elif Admitting_Service in ( 'Neurosurgery') or Discharge_Service in ('Neurosurgery'):
        service = 'Neurosurgery'
    elif Admitting_Service in ( 'Orthopaedics') or Discharge_Service in ('Orthopaedics'):
        service = 'Ortho'
    elif Admitting_Service in ( 'Otolaryngology' 'Oral Surgery') or Discharge_Service in (
                                'Otolaryngology' 'Oral Surgery'):
        service = 'ENT_oral'
    elif Admitting_Service in ('Ophthalmology' )or Discharge_Service in ('Ophthalmology'):
        service = 'Ophthalmology'
    elif pr1 in (   '0051' ,'0054' ,'0061' ,'0066' ,'331' ,'3734','3776', '3201', '3321', '3324', '3326', '3327','3328' ,'3351', '3352', '343' ,'346', '3491',
                    '3512' ,'3521' ,'3533' ,'3562' ,'3613','3721','3722', '3723', '3724', '3726', '375' ,'3761' ,'3712' ,'3751', '3766', '3774', '3777', '3779', '3783', '3789', '3794', '3796', '3798',
                    '3799' ,'3818' ,'3821' ,'3843' ,'3844','387' ,'3893', '391' , '3927', '3943', '3949', '3950', '3951','3979', '3995','3998'):
        service = 'CT_Surgery'
    elif pr1 in (   '0112', '0113', '0114', '0122', '0125', '0131', '0139', '0151', '0159', '022',
                    '0234', '0242', '0309', '0332', '0359', '0412'):
        service = 'Neurosurgery'
    elif pr1 in (   '062' , '0691', '0782', '4011', '4023', '4029', '403', '4105', '4106', '415', '8512', '8521'):
        service = 'General_Oncology'
    elif pr1 in (   '0852', '1269', '1662', '1681', '1682',):
        service = 'Ophthalmology'
    elif pr1 in (   '2263', '245' , '248' , '2811', '311' '3129' '3143' '3199'):
        service = 'ENT_oral'
    elif pr1 in (   '4285' ,'4292' ,'4415' ,'4432' ,'4443' ,'4603' ,'5019' ,'5110' ,'5122' ,'5123' ,'5184' ,'5185' ,'5188' ,'5198' ,'5201' ,'5211' ,'5293',
                    '5349' ,'5411' ,'5419' ,'5423' ,'5459' ,'5491' ,'5493' ,'5495' ,'9705'):
        service = 'General_GI'
    elif pr1 in (   '4513', '4516', '4516' ,'4523' ,'4525' ,'4542' ,'4562' ,'4573' ,'4579' ,'458' ,'4711' ,'4871' ,'4881' ,'4901'):
        service = 'General_Colorectal'
    elif pr1 in (   '5503' ,'5504' ,'5523' ,'5539' ,'5551' ,'560' ,'570' ,'5717' ,'5718' ,'5732' ,'5733'
                    '5749' ,'5793' ,'5794' ,'585' ,'586' ,'598' ,'6029' ,'605' ,'6241' ,'6029' ,'6241'):
        service = 'Urology'
    elif pr1 in (   '7674', '7676', '7741', '7749', '7761', '7769', '7785', '7855', '7906', '7915',
                    '7932', '7935', '7935', '7936', '7937', '8011', '8037', '8051', '8076', '8084', '8105',
                    '8151', '8152', '8309', '8321', '8345', '8382', '8401', '8411', '8412', '8415', '8416', '8417'):
        service = 'Ortho'
    elif pr2 in (   '0051' ,'0054' ,'0061' ,'0066' ,'331' , '3734', '3776', '3201', '3321', '3324', '3326', '3327',  '3328', '3351', '3352', '343', '346', '3491',
                    '3512' ,'3521' ,'3533' ,'3562' ,'3613', '3721', '3722', '3723', '3724', '3726', '375', '3761', '3712', '3751', '3766', '3774', '3777', '3779', '3783',
                    '3789' ,'3794' ,'3796' ,'3798' ,'3799', '3818', '3821', '3843', '3844', '387', '3893', '391', '3927', '3943', '3949', '3950', '3951', '3979', '3995', '3998'):
        service = 'CT_Surgery'
    elif pr2 in (   '0112', '0113', '0114', '0122', '0125', '0131', '0139', '0151', '0159', '022',
                    '0234', '0242', '0309', '0332', '0359', '0412'):
        service = 'Neurosurgery'
    elif pr2 in (   '062', '0691', '0782', '4011', '4023', '4029' ,'403' ,'4105' ,'4106' ,'415' ,'8512' ,'8521'):
        service =   'General_Oncology'
    elif pr2 in (   '0852' ,'1269' ,'1662' ,'1681' ,'1682'):
        service = 'Ophthalmology'
    elif pr2 in (   '2263' ,'245' ,'248' ,'2811', '311', '3129', '3143', '3199'):
        service = 'ENT_oral'
    elif pr2 in (   '4285' ,'4292' ,'4415' ,'4432' ,'4443' ,'4603' ,'5019' ,'5110' ,'5122' ,'5123' ,'5184' ,'5185' ,'5188' ,'5198' ,'5201' ,'5211', '5293'
                    '5349' ,'5411' ,'5419' ,'5423' ,'5459' ,'5491' ,'5493' ,'5495' ,'9705'):
        service = 'General_GI'
    elif pr2 in (   '4513' ,'4516' ,'4516' ,'4523' ,'4525' ,'4542' ,'4562' ,'4573' ,'4579' ,'458' ,'4711' ,'4871' ,'4881' ,'4901'):
        service = 'General_Colorectal'
    elif pr2 in (   '5503', '5504', '5523', '5539', '5551', '560', '570', '5717', '5718', '5732', '5733',
                    '5749', '5793', '5794', '585', '586', '598', '6029', '605', '6241',
                    '6029', '6241'):
        service = 'Urology'
    elif pr2 in (   '7674', '7676', '7741', '7749', '7761', '7769', '7785', '7855', '7906', '7915',
                    '7932', '7935', '7935', '7936', '7937', '8011', '8037', '8051', '8076', '8084', '8105',
                    '8151', '8152', '8201', '8235', '8309', '8321', '8344', '8345', '8382', '8401', '8411', '8412','8415', '8416', '8417'):
        service = 'Ortho'
    elif pr2 in ('6991'):
        service = 'OB_GYN';
    elif pr1 in ( '9227','9229', '9604', '9671', '9672', '9915', '9925', '9929'):
        service = 'nonoperative'
    else :
        service = 'other'

    if service in ("General_Colorectal","General_GI" ,"General_Oncology" ,"Vascular"):
        service1 = "Non-Cardiac General Surgery"
    elif service in ("Neurosurgery") :
        service1 = "Neurologic Surgery"
    elif service in ("Ortho" ,"ENT_oral" ,"Plastic" ,"Urology" ,"OB_GYN"):
        service1 = "Specialty Surgeries"
    elif service in ("CT_Surgery"):
        service1 = "Cardiothoracic surgery"
    elif service in ( "Burn" , 'other' , 'nonoperative', "Transplantation", "Ophthalmology" ,"Trauma"):
        service1 = "Other surgeries"

    return service1


def mark_as_ped(Discharge_Service ,Admitting_Service):
    if Discharge_Service in ('Ped Critical Care',
                             'Pediatric Endocrinology',
                             'Pediatric Gastroenterology',
                             'Ped Critical Care',
                             'Pediatric Endocrinology',
                             'Pediatric Gastroenterology',
                             'Pediatric Hematology/Oncology',
                             'Pediatric Immuno. & Inf. Dis.',
                             'Pediatric Nephrology',
                             'Pediatric Neurology',
                             'Pediatric Pulmonary',
                             'General Pediatrics',
                             'Surgery, Pediatric',
                             'Ped Critical Care',
                             'Pediatric Hematology/Oncology',
                             "Children's Hospital Heart Cntr") or Admitting_Service in ('Ped Critical Care',
                                                                                        'Pediatric Endocrinology',
                                                                                        'Pediatric Gastroenterology',
                                                                                        'Ped Critical Care',
                                                                                        'Pediatric Endocrinology',
                                                                                        'Pediatric Gastroenterology',
                                                                                        'Pediatric Hematology/Oncology',
                                                                                        'Pediatric Immuno. & Inf. Dis.',
                                                                                        'Pediatric Nephrology',
                                                                                        'Pediatric Neurology',
                                                                                        'Pediatric Pulmonary',
                                                                                        'General Pediatrics',
                                                                                        'Surgery, Pediatric',
                                                                                        'Ped Critical Care',
                                                                                        'Pediatric Hematology/Oncology',
                                                                                        'Pediatric Cardiology',
                                                                                        'Pediatric Surgery',
                                                                                        "Children's Hospital Heart Cntr"):
        return 1
    else:
        return 0

