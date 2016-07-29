#!/bin/bash
# file: exportid.sh	G. Moody			16 February 2011
#	modified	I. Silva			 7 April    2011		
# Export a set of flat files for a single subject

# This script creates a directory named NNNNN (the zero-padded subject id)
# and then creates a set of flat files for the chosen subject in NNNNN.
# To keep this script relatively fast and simple, it produces files that
# include these quirks:
#  * Fields are never quoted
#  * Embedded commas are escaped with backslashes:  , -> \,
#  * Multiline inputs create multiline output (since fields aren't quoted)

# The zero-padded subject id
SID=$1

# Strip leading zeroes to get ID (subject_id)
ID=`echo $SID | sed 's/0*//'`

# Create the directory
mkdir -p $SID
chmod 777 $SID

# Export the subject's data
#Modified by Ikaro to include new tables from MIMIC II 2v26
for TAB in D_PATIENTS ADMISSIONS POE_ORDER ICUSTAYEVENTS \
	  A_CHARTDURATIONS CENSUSEVENTS MEDEVENTS ADDITIVES \
	  CHARTEVENTS NOTEEVENTS DELIVERIES POE_MED A_IODURATIONS \
	  IOEVENTS A_MEDDURATIONS ICD9 LABEVENTS TOTALBALEVENTS \
	  ICUSTAY_DAYS ICUSTAY_DETAIL COMORBIDITY_SCORES DRGEVENTS \
          MICROBIOLOGYEVENTS DEMOGRAPHIC_DETAIL DEMOGRAPHICEVENTS \
          PROCEDUREEVENTS WAVEFORM_METADATA WAVEFORM_SEG_SIG WAVEFORM_SEGMENTS \
          WAVEFORM_SIGNALS WAVEFORM_TREND_SIGNALS WAVEFORM_TRENDS
do
    TF=$PWD/$SID/${TAB}-$SID.txt
    psql MIMIC2 -c "SELECT * FROM MIMIC2V26.$TAB WHERE SUBJECT_ID=$ID;" |
      sed -e "s/,/\\\\,/g; s/ *+*| */,/g; s/^ *//; 2d" | head -n -2 >$TF
    if [[ `wc -l <$TF` = 1 ]]
    then
	cp /dev/null $TF
    fi
done
