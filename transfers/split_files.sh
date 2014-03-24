#FILELISTS_DIR="Filelists_data_el"
FILELISTS_DIR="TransfersForResubmit_mu"
LINES_PER_FILE=100

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
  split -l $LINES_PER_FILE $FILELIST ../$SPLIT_DIR$FILELIST_SPLIT"_part_" 
done