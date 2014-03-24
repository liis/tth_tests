#!/bin/bash

INDIR="TransfersForResubmit_quick"
SRMPATH="srm://ganymede.hep.kbfi.ee:8888/srm/v2/server?SFN="

DELETELISTS=`ls $INDIR/delete_list*.txt` 

voms-proxy-init -voms cms
for DELETE_LIST in $DELETELISTS #`ls $INDIR"/delete_list*.txt"`
do
  echo "Scanning delete-list: "`basename $DELETE_LIST`
  while read line
    do
    echo "Removing: "$line
    srmrm $SRMPATH$line 

  done < $DELETE_LIST
done  # scan of delete lists