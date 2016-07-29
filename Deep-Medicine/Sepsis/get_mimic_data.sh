#!/bin/bash
# file: get_mimic_data.sh	Ikaro Silva May 2011
#                               Daniel Scott (djscott@mit.edu)
# Link to get files from PhysioNetWorks

PHYSIONETWORKS_URI="https://physionet.org/works/mimic2cdb/files/"
PHYSIONET_URI="http://physionet.org/mimic2/flat_files/"

#Options for verision are latest, mimic2v25, and mimic2v26
FILE="get_"
VERSION="latest"                                        
#File extension
EXT=".txt"
PT_START=1
data_sufix="mimic2cdb-"
#Leave empty for all (default)
PT_END=
CONFIG_VM="n"                            # configures the VM after download is complete
VM_HOST="mimic2"
IMPORT_TAG="Importer"

# Parse command line arguments
while [ -n "($echo $1 | grep '-')" ]; do
    case $1 in
	-u )username=${2:?" username missing."}
	    shift ;;
	-c )CONFIG_VM="y"     #Flag for configuring the VM 
	    ;;
	-v )VERSION=${2:?" version missing."}
	    shift ;; 
	-h ) echo "usage: $0 -u username [-h] [-c configure the MIMIC 2 virtual machine]";
     	    exit 1 ;;
	*) break ;;
    esac
    shift
done

if [ -z ${username} ]; then
    read -p "Enter your PhysioNetWorks username: " username
fi

# If VM configuration flag is passed, check to see if we are in the MIMIC 2 VM 
if [ "${CONFIG_VM}" == "y" ]; then
    THIS_HOST=`hostname`
    if [ "${THIS_HOST}" != "${VM_HOST}" ]; then
	echo "Error: Not a MIMIC 2 Virtual Machine Environment. Remove the -c flag from command."
	exit
    fi
    IMPORT_DIR="/tmp"

    # In -c mode, download everything to the IMPORT_DIR directory
    cd ${IMPORT_DIR}
else
    IMPORT_DIR="."
fi

echo Downloading files to ${IMPORT_DIR}

#Download package list from server
PHYS_FNAME=${PHYSIONET_URI}${FILE}${VERSION}${EXT} 
FNAME=${FILE}${VERSION}${EXT} 
echo "----------------------------------------"
echo "Starting MIMIC II Download of latest packages..."
echo "*** You will be asked to log into PhysioNetWorks "
echo "----------------------------------------"
if [ -e ${FNAME} ]; then
    rm ${FNAME} 
fi
wget ${PHYS_FNAME} 
if [ "$?" -ne "0" ];then
    echo "Could not connect to PhysioNet. Please check your network connection and try again."
    exit
fi

# Preprocess the package file
# Checking if they are in the desired range 
N=`cat ${FNAME} | wc -l`
if [[ -z ${PT_END} ]] ; then
    PT_END=${N}
fi
TAIL=$(( ${PT_END} - ${PT_START} + 1 ))
cat ${FNAME} | head -n ${PT_END} | tail -n ${TAIL} > get_mimic.tmp # Store package list in temporary file

# Remove any data packages that has already been downloaded on the current directory
# (THIS WILL NOT REMOVE PDFs other packages  in another directory from {data_sufix} !)
PHYS_DIR=`dirname $( cat get_mimic.tmp | grep ${data_sufix} | tail -n1 )`
cat get_mimic.tmp > get_mimic2.tmp
find . -type f -printf "${PHYS_DIR}/%f\n" > get_mimic_rep.tmp
comm -23 <(sort get_mimic2.tmp) <(sort get_mimic_rep.tmp) >get_mimic.tmp
TAIL2=`cat get_mimic.tmp | wc -l`
TAILDIFF=$(( ${TAIL} - ${TAIL2} ))
echo "Downloading packages between ${PT_START} and ${PT_END}"
echo "Total packages left: ${TAIL2} ( ${TAILDIFF} packages previously downloaded ) ..."  

if test ! "${TAIL2}" -eq "0";then
    #Download any packages that are left to download
    wget --ask-password --user=${username} -i get_mimic.tmp 
    if [ "$?" -ne "0" ]; then
	echo "Could not connect to your PhysioNetWorks account. Check: account username, password, and/or connection."     echo "Some files NOT downloaded. Exiting Script"
	exit
    fi
fi

echo "----------------------------------------"
echo "----- MIMIC 2 Download Complete !  -----"
echo "----------------------------------------"
echo ""

rm -f get_mimic.tmp
rm -f get_mimic_rep.tmp
rm -f get_mimic2.tmp

#VM configuration flag is passed, check to see if we are in the MIMIC 2 VM 
if [ "${CONFIG_VM}" == "y" ]; then
    echo "----------------------------------------"
    echo "----- Starting VM Configuration    -----"
    echo "----------------------------------------"

    echo "Moving Documentation, SQL Examples and User Guide to Desktop..."
    mv *.pdf ~/Desktop/
    # Move SQL examples to desktop unless it already exists
    if [ ! -e ~/Desktop/sql_examples ]; then
	tar xf sql_examples.tar.gz
	mv sql_examples ~/Desktop/
    fi
    rm sql_examples.tar.gz

    IMPORTER_TAR=`basename $(cat ${FNAME} | grep ${IMPORT_TAG})`
    if [ -z ${IMPORTER_TAR} ]; then
	echo "Error: Importer Tool ${IMPORTER_TAR} not available from PhysioNetWorks for this version."
	exit
    fi
    
    #echo "Moving tarballs to the ${IMPORT_DIR} directory..." --should already be in this directory
    #rsync -v ${IMPORTER_TAR} ${IMPORT_DIR}

    echo "Unpacking the MIMIC II Importer (${IMPORTER_TAR}) in ${IMPORT_DIR} ..."
    tar xf ${IMPORTER_TAR} -C ${IMPORT_DIR}
   
    if [ "$?" -ne "0" ]; then
	echo "Error: Could not unpack Importer Tool. Check download of ${IMPORTER_TAR} ..."
	exit
    fi 

    # Moving tarballs into importer directory
    echo Moving tarballs into ${IMPORT_DIR}/`basename ${IMPORTER_TAR} .tar.gz`
    mv ${IMPORT_DIR}/${data_sufix}*.tar.gz ${IMPORT_DIR}/`basename ${IMPORTER_TAR} .tar.gz`

    echo ****To start importing the MIMIC II Importer enter the following commands:
    echo cd ${IMPORT_DIR}/`basename ${IMPORTER_TAR} .tar.gz`
    echo sudo ./prep.sh
    echo ./import.sh

fi 
