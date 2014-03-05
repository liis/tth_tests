#FILELISTS_DIR="Filelists_data"
FILELISTS_DIR="TransfersForResubmit"
SPLIT_DIR=$FILELISTS_DIR"_split/"

mkdir $SPLIT_DIR
rm $SPLIT_DIR/*_part*

cd $FILELISTS_DIR
FILELISTS=`ls *.txt`
echo Saving split filelists to $SPLIT_DIR

echo `pwd`
echo $FILELISTS
for FILELIST in $FILELISTS
do
  echo Opening input file $FILELIST with nr. files `wc -l $FILELIST`

  FILELIST_SPLIT=${FILELIST%.*} #drop .txt (drop after '.')
  split -l 30 $FILELIST ../$SPLIT_DIR$FILELIST_SPLIT"_part_" 
done