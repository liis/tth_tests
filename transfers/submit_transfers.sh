FILELISTS_DIR="VHbb_transfer/WJets"

FILELISTS=`ls $FILELISTS_DIR/*.txt`

for FILELIST in $FILELISTS:
do
  OUTDIR=$(basename $FILELIST)
  OUTDIR=${OUTDIR#*_}
  OUTDIR=${OUTDIR%%.*}

  screen -d -m -S $OUTDIR 
  echo transfering filelist $FILELIST to outdir $OUTDIR

  CMD="screen -S $OUTDIR -p 0 -X exec sh data_transfer.sh $FILELISTS_DIR $OUTDIR" #execute in parallel screens

#  CMD="sh data_transfer.sh $FILELISTS_DIR $OUTDIR"
# CMD="qsub -q all.q data_transfer.sh $FILELISTS_DIR $OUTDIR" # try to run as a batch job, but data_replica.py fails (not understood)  

  echo submitting: $CMD
  eval $CMD

done