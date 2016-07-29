#!/bin/bash
# file: import.sh       Ikaro Silva, George Moody	13 February 2011
#                       and Daniel Scott
#			Last revised:			 19 May 2011
# The MIMIC Importer: Create or update MIMIC2 database from flat files

# If you run the MIMIC Importer like this:
#	./import.sh | tee import.log
# ... you can view its progress and also create a log file to examine later.

# This script should be run while logged in as the user who is (or will be)
# the "owner" of the MIMIC2 relational database, not as root.  Before running
# it the first time, however, run the script "prep.sh", which does require root
# permissions.

# ### The first part of this script initializes the database the first time it
# is run.  On subsequent runs (to load additional subjects), it only checks to
# see that this has been done.

# Create a directory for saving the tarballs after processing (for reuse).
if ! [ -d tarballs ]
then
    mkdir tarballs
fi

# Unpack the definitions first if necessary.
DEFTARBALL=mimic2cdb-2.6-Definitions.tar
if [ -s $DEFTARBALL.gz ]
then
    tar xfz $DEFTARBALL.gz
    mv $DEFTARBALL.gz tarballs
elif [ -s $DEFTARBALL ]
then
    tar xf $DEFTARBALL
    mv $DEFTARBALL tarballs
elif [ ! -d Definitions ]
then
    echo Please download mimic2cdb-2.6-Definitions.tar.gz and try again.
    exit
fi

echo
date
echo

# Create MIMIC2 database if it doesn't exist already
if psql --list | grep MIMIC2 >/dev/null
then
    echo "Data will be imported into the existing MIMIC2 database."
    echo -n " Continue? [y/N]: "
    read ANSWER
    case $ANSWER in
	y*|Y*) echo "OK, starting import." ;;
	    *) echo "Cancelled, MIMIC2 has not been changed."
	    exit ;;
    esac
else
    echo "Creating MIMIC2 ..."
    createdb MIMIC2
    DBDIR=`./data-directory-name.sh`/mimic2v26_dat
    echo "Assigning $DBDIR to MIMICV26 tablespace ..."
    psql MIMIC2 -q -c "CREATE TABLESPACE MIMIC2V26_DAT LOCATION '$DBDIR';"
    echo "Loading the MIMIC2V26 schema ..."
    psql MIMIC2 -q -f `pwd`/Definitions/POSTGRES/schema_mimic2v26.sql
    echo "Loading the table definitions ..."
    for DFILE in `pwd`/Definitions/*.txt
    do
	DEF=`basename $DFILE .txt`
	echo $DEF
	SQL_CMD="COPY MIMIC2V26.$DEF FROM '$DFILE' WITH DELIMITER E',' \
                 CSV HEADER;"
	psql MIMIC2 -q -c "$SQL_CMD"
    done
fi

echo
date
echo

# ### The second part of this script begins here.  This part loads subject-
# specific data from the flat files into the MIMIC2 relational database.
# If you don't want to load the entire database at once, you can restrict
# the range of subject IDs to process using the -s and -e options.  You
# can also download only a subset of the subject-specific tarballs into
# this directory before running this script.  By default, all of the
# available subject-specific flat files are loaded.
#
# After each tarball is unpacked, it is moved aside so that it won't be
# unpacked again on a subsequent run.  After each set of subject-specific
# flat files is loaded, it is removed so that this script will not attempt
# to reload it on a subsequent run (and to minimize the workspace requirements).


# Determine the range of subject IDs to process (default: all)

START=0
END=0

for ARG in $*
do
    case $ARG in
	-s) shift; START=$1; shift ;;
	-e) shift;   END=$1; shift ;;
    esac
done

if [[ $END -lt 1 || $END -gt 99999 ]]
then
    END=99999
elif [[ $END -lt $START ]]
then
    T=$END
    END=$START
    START=$T
else
    END=`expr $END + 1`
fi
if [[ $START -lt 1 ]]
then
    START=0
else
    START=`expr $START - 1`
fi
FIRST=`printf %05d $START`
LAST=`printf %05d $END`
NNFIRST=`echo FIRST | cut -c1-2`
NNLAST=`echo LAST | cut -c1-2`

echo
date
echo

echo "Subject IDs between $FIRST and $LAST will be processed."

# Load the subject-specific data
for NN in 00 01 02 03 04 05 06 07 08 09 \
          10 11 12 13 14 15 16 17 18 19 \
          20 21 22 23 24 25 26 27 28 29 \
          30 31 32
do
  TFIRST=${NN}000
  TLAST=${NN}999
  if [[ $TLAST < $FIRST || $TFIRST > $LAST ]]
  then
    continue; # this set does not include any subjects of interest
  fi
    
  TARBALL=mimic2cdb-2.6-${NN}.tar
  if [ -s $TARBALL.gz ]
  then
    echo "Unpacking ${TARBALL} ..."
    tar xfz $TARBALL.gz
    mv $TARBALL.gz tarballs
  elif [ -s $TARBALL ]
  then
    echo "Unpacking ${TARBALL} ..."
    tar xf $TARBALL
    mv $TARBALL tarballs
  fi

  if [ ! -d $NN ]
  then
    echo "Warning: set ${NN} not available"
    continue; # this set is not available
  fi

  cd $NN
  TMP_N=`find . -maxdepth 1 -type d | wc -l`
  echo Processing set ${NN} with $(( ${TMP_N}-1 )) subjects at `date`
  jobsrunning=0
  maxjobs=10
  for ID in ?????
  do
      if [ $jobsrunning -eq $maxjobs ]; then
	  jobsrunning=0
	  wait
      fi
      jobsrunning=$(( $jobsrunning+1 ))
      if [[ $FIRST < $ID && $ID < $LAST ]]; then    
	  (( for TAB in D_PATIENTS ADMISSIONS ICUSTAYEVENTS \
	      A_CHARTDURATIONS CENSUSEVENTS MEDEVENTS ADDITIVES \
	      CHARTEVENTS NOTEEVENTS DELIVERIES POE_ORDER POE_MED A_IODURATIONS \
	      IOEVENTS A_MEDDURATIONS ICD9 LABEVENTS TOTALBALEVENTS \
	      DRGEVENTS MICROBIOLOGYEVENTS \
              DEMOGRAPHICEVENTS PROCEDUREEVENTS \
	      ICUSTAY_DAYS ICUSTAY_DETAIL COMORBIDITY_SCORES DEMOGRAPHIC_DETAIL
            do
                TF=$PWD/$ID/${TAB}-$ID.txt
		if [ -d "$PWD/$ID/" -a -s $TF ]; then
		    echo "COPY MIMIC2V26.$TAB FROM '$TF' WITH DELIMITER E',' CSV HEADER;"
	        fi
            done
	  ) | psql MIMIC2 -q -f -
          # remove each subject's flat files when no longer needed
	  rm -rf $ID) &
      fi
  done
  cd ..
  echo
  LOADED=`psql MIMIC2 -tc "select count(distinct(subject_id)) from mimic2v26.d_patients;"`
  echo Total subjects added: $LOADED for batch $NN at `date`
  
done

echo Creating the indices ... at `date`
psql MIMIC2 -q -f `pwd`/Definitions/POSTGRES/indices_mimic2v26.sql

echo ***Done creating the MIMIC II Database at `date`
