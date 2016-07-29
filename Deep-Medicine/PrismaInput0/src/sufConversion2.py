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
        date_object = datetime.strptime(date, '%m/%d/%Y')
        days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dayNumber=date_object.weekday()
        return days[dayNumber]
    except ValueError:
        return "Unknown"

def month(date):
    try:
        date_object = datetime.strptime(date, '%m/%d/%Y')
        days=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","n/a"]
        dayNumber=date_object.weekday()
        return days[dayNumber]
    except ValueError:
        return "Unknown"


def year(date):
    try:
        date_object = datetime.strptime(date, '%m/%d/%Y')
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


