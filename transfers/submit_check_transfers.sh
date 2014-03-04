#!/bin/bash

INFILELIST_DIR="VHbb_transfer/from_lorenzo"
OUTPUT_FILE_DIR="TransfersForResubmit"
RUN_DATA_REPLICA=0
SUBMIT_TO_BATCH=1

if [ RUN_DATA_REPLICA == 1 ] ; then
    PYTHONHOME="/usr/lib/python2.6"
fi

voms-proxy-init -voms cms

for INFILELIST in `ls -d -1 $INFILELIST_DIR/**` # take whole path
  do
  
  echo Start processing $INFILELIST
  
  if [ $SUBMIT_TO_BATCH == 1 ] ; then
      echo "Submitting to batch"
      chmod +x check_file_transfers.sh
      qsub check_file_transfers.sh $INFILELIST $RUN_DATA_REPLICA
  else
      sh check_file_transfers.sh $INFILELIST $RUN_DATA_REPLICA
  fi
  
done

