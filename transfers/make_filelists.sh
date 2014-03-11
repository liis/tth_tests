#!/bin/bash

INDIR="/hdfs/cms/store/user/liis/VHbb_patTuples/"
OUTDIR="./"
#OUTDIR="./filelists"

echo Getting filelists from $INDIR
for DATASET in `ls $INDIR`
do
  echo Analysisng $DATASET
  ls -d -1 $INDIR$DATASET/** > $OUTDIR/filelist_$DATASET".txt"
done
