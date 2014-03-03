#!/bin/bash

INFILELIST_DIR="VHbb_transfer/from_lorenzo"
OUTPUT_FILE_DIR="TransfersForResubmit"

for INFILELIST in `ls -d -1 $INFILELIST_DIR/**` # take whole path
  do
  
  echo Start processing $INFILELIST
  sh check_file_transfers.sh $INFILELIST $OUTPUT_FILE_DIR

done

