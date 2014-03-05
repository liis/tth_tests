#!/bin/bash

INFILELIST_DIR=$1

for INFILELIST in `ls -d -1 $INFILELIST_DIR/**` # take whole path
  do
  
  echo Start processing $INFILELIST
  sh check_file_transfers_quick.sh $INFILELIST $RUN_DATA_REPLICA
    
done

