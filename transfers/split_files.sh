FILELISTS_DIR="VHbb_transfer/WJets"


cd $FILELISTS_DIR
FILELISTS=`ls *.txt`

echo `pwd`
echo $FILELISTS
for FILELIST in $FILELISTS
do
  echo Opening input file $FILELIST with nr. files `wc -l $FILELIST`


#  OUTDIR=$(basename $FILELIST)
#  OUTDIR=${OUTDIR#*_}
#  OUTDIR=${OUTDIR%%.*}

#  split -l 100 $FILELIST $OUTDIR"_" 
done