#!/bin/bash

INIT_SRMPATH="srm://stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms" # initial location of copied files
INFILELIST=$1
#INFILELIST="VHbb_transfer/fileList_SingleElectronRun2012AAug06EdmV42.txt" #filelist with input filenames (including full paths) --> take as argument


DEST_SRMPATH="srm://ganymede.hep.kbfi.ee:8888/srm/v2/server?SFN="
DEST_PATH="/hdfs/cms/store/user/liis/VHbb_patTuples/"

OUTDIR=`basename $INFILELIST}` #get after last '/'
OUTDIR=${OUTDIR%.*} #drop .txt (drop after '.')
OUTDIR=${OUTDIR#*_} #drop fileList_ (drop before first '_')

#echo OUTDIR = $OUTDIR 
#OUTDIR="SingleElectronRun2012AAug06EdmV42" #defined by INFILELIST NAME, use for debug


echo Getting file-lists from final directory: $DEST_SRMPATH$DEST_PATH$OUTDIR
FILENAMES_DEST=(`srmls -l %s $DEST_SRMPATH$DEST_PATH$OUTDIR | awk '{print $2}'`) #Get first/2nd part of the output
FILESIZES_DEST=(`srmls -l %s $DEST_SRMPATH$DEST_PATH$OUTDIR | awk '{print $1}'`) # put parentheses to indicate an array
FILESIZES_DEST=("${FILESIZES_DEST[@]:1}") # remove the first element (name of directory)

NR_FILESIZES_DEST=${#FILESIZES_DEST[@]} #get nr of files
NR_FILENAMES_DEST=${#FILENAMES_DEST[@]}
if [ $NR_FILESIZES_DEST != $NR_FILENAMES_DEST ]; then # sanity chech
    echo WARNING nrFilenames = $NR_FILENAMES_DEST , nrFilesizes = $NR_FILESIZES_DEST -- dont match!
fi


######## initialize output file###########
fail_list="fail_list_"$OUTDIR".txt"
if [ ! -f "$fail_list" ] ; then
    touch "$fail_list"
else
    >$fail_list #empty existing content
fi
###############

echo "Loop over files in infilelist $INFILELIST"
while read line
do
  SIZE_INIT=`srmls -l %s $INIT_SRMPATH$line | awk '{print $1}'`
  FILE_INIT=`basename $line`
  echo Matching initial file $FILE_INIT with size $SIZE_INIT

  MATCH_INIT_DEST=0
  SIZE_INIT_DEST=0
  
  for (( i=0; i<$NR_FILESIZES_DEST; i++)) #Loop over files at destination
    do
    FILE_DEST=`basename ${FILENAMES_DEST[$i]}`
    SIZE_DEST=${FILESIZES_DEST[$i]} 
    if [ $FILE_DEST == $FILE_INIT ]; then #Check whether the file exists at destination
	MATCH_INIT_DEST=1
	SIZE_DEST_MATCHED=$SIZE_DEST
    fi
    
    if [ $FILE_DEST == $FILE_INIT ]  && [ $SIZE_DEST_MATCHED == $SIZE_INIT ]; then
	SIZE_INIT_DEST=1
    fi
    
  done

#  echo MATCH_INIT_DEST = $MATCH_INIT_DEST
#  echo SIZE_INIT_DEST = $SIZE_INIT_DEST

  if [ $MATCH_INIT_DEST == 1 ] && [ $SIZE_INIT_DEST == 1 ]; then # Resubmit transfer, if needed
      echo Transfer OK

  elif [ $MATCH_INIT_DEST == 1 ] && [ $SIZE_INIT_DEST == 0 ]; then 
      echo "Match found but broken transfer (size_init != size_dest )"
      echo "Size init = $SIZE_INIT, size dest = $SIZE_DEST_MATCHED --> Clean up and resubmit copy!"
      echo "$line" >> $fail_list
  else
      echo "No match found --> resubmit copy!"
      echo "$line" >> $fail_list
  fi

done < $INFILELIST 
