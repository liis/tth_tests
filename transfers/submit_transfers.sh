#!/bin/bash  

FILELISTS=`cat $1` #a text file
#echo $FILELISTS

for FILELIST in $FILELISTS:
do
  OUTDIR=$FILELIST
  OUTDIR=${OUTDIR#*_}
  OUTDIR=${OUTDIR%%.*}

  echo outdir = $OUTDIR
 #   echo transfering filelist $FILELIST to outdir $OUTDIR

#  voms-proxy-init -voms cms
#    screen -d -m -S $OUTDIR 
#  CMD="screen -S $OUTDIR -p 0 -X exec sh data_transfer.sh $FILELISTS_DIR $OUTDIR" #execute in parallel screens
#  CMD="sh data_transfer.sh $FILELISTS_DIR $OUTDIR" #execute in sequence in the same window

#    CMD="qsub -V -cwd data_transfer.sh $FILELISTS_DIR $OUTDIR" # try to run as a batch job, but data_replica.py fails (not understood)  

#    echo submitting: $CMD
#  eval $CMD
done