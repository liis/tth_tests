#!/bin/bash

INFILELIST_DIR="Filelists_data_el"
#INFILELIST_DIR="TransfersForResubmit_mc" # where to save output file lists
OUTPUT_FILE_DIR="TransfersForResubmit_el" # where to save output file lists
RUN_DATA_REPLICA=0 # whether or not submit data_replica.py to get missing files (otherwise save missing files in file)
SUBMIT_TO_BATCH=1


if [ RUN_DATA_REPLICA == 1 ] ; then
    PYTHONHOME="/usr/lib/python2.6" #not needed if you avoid cmsenv 
fi

voms-proxy-init -voms cms
echo outputdir = $OUTPUT_FILE_DIR

for INFILELIST in `ls -d -1 $INFILELIST_DIR/**` # take whole path
  do
  
  echo Start processing $INFILELIST
  
  if [ $SUBMIT_TO_BATCH == 1 ] ; then
      echo "Submitting to batch"
      chmod +x check_file_transfers.sh
      qsub check_file_transfers.sh $INFILELIST $RUN_DATA_REPLICA $OUTPUT_FILE_DIR
  else
      sh check_file_transfers.sh $INFILELIST $RUN_DATA_REPLICA $OUTPUT_FILE_DIR
  fi
  
done

