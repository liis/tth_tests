#!/bin/bash

INIT_SRMPATH="srm://stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms" # initial location of copied files
INFILELIST=$1
RUN_AT_DEST=1 # When run at destination, can do ls instead of srmls

SUPERQUICK=1

DEST_SRMPATH="srm://ganymede.hep.kbfi.ee:8888/srm/v2/server?SFN="
DEST_PATH="/hdfs/cms/store/user/liis/VHbb_patTuples/"

OUTDIR=`basename $INFILELIST}` #get after last '/' -- where output is stored at destination
OUTDIR=${OUTDIR%.*} #drop .txt (drop after '.')
#OUTDIR=${OUTDIR#*_} #drop fileList_ (drop before first '_')

#echo OUTDIR = $OUTDIR 

######## initialize output file###########
OUTPUT_FILES_DIR="TransfersForResubmit_quick"
fail_list="$OUTPUT_FILES_DIR/fail_list_"$OUTDIR".txt" #read dir for output files from the argument
delete_list="$OUTPUT_FILES_DIR/delete_list_"$OUTDIR".txt"

if [ ! -f "$fail_list" ] ; then
    touch "$fail_list"
else
    >$fail_list #empty existing content
fi
if [ ! -f "$delete_list" ] ; then
    touch "$delete_list"
else
    >$fail_list #empty existing content
fi

###############   



if [ $RUN_AT_DEST == 1 ]; then
    echo Getting file-list from final directory: $DEST_PATH$OUTDIR
    FILENAMES_DEST=(`ls -la $DEST_PATH$OUTDIR/*.root | awk '{print $9}'`)
else
    echo Getting file-list from final directory: $DEST_SRMPATH$DEST_PATH$OUTDIR
    FILENAMES_DEST=(`srmls -l %s $DEST_SRMPATH$DEST_PATH$OUTDIR | awk '{print $2}'`) #Get first/2nd part of the output
fi

NR_FILENAMES_DEST=${#FILENAMES_DEST[@]}
if [ $NR_FILENAMES_DEST == 0 ]; then
    echo "Full Directory missing at destination --> resubmit full file-list -> EXITING."
    cat $1>$fail_list

    exit 1
fi

echo ...done

NR_INIT_FILES=`wc -l $INFILELIST | awk '{print $1}'`
echo $NR_INIT_FILES present at initial site, $NR_FILENAMES_DEST copied to destination

if [ $SUPERQUICK == 0 ]; then
    echo Missing files:
    while read line
      do
      FILE_INIT=`basename $line`
      
      MATCH_INIT_DEST=0
      for (( i=0; i<$NR_FILENAMES_DEST; i++)) #Loop over files at destination
	do
	FILE_DEST=`basename ${FILENAMES_DEST[$i]}`
	if [ $FILE_DEST == $FILE_INIT ]; then #Check whether the file exists at destination
	    MATCH_INIT_DEST=1
	fi
      done

      if [ $MATCH_INIT_DEST == 0 ]; then
	  echo $line
	  echo $line >> $fail_list
      fi

    done < $INFILELIST 
    echo Done scanning for missing files
fi

if [ $SUPERQUICK == -1 ]; then
    echo Checking for additional files to delete:

    for (( i=0; i<$NR_FILENAMES_DEST; i++)) #Loop over copied files                                    
      do

      FILE_DEST=`basename ${FILENAMES_DEST[$i]}`
      MATCH_INIT_DEST=0
      while read line
	do
	FILE_INIT=`basename $line`
	if [ $FILE_DEST == $FILE_INIT ]; then #Check whether the file exists in file list                        
	    MATCH_INIT_DEST=1
	    echo found match for file: $FILE_DEST
	fi
      done < $INFILELIST      

      if [ $MATCH_INIT_DEST == 0 ]; then # if no match found in the file list, write to delete_list
	  echo No match found for file ${FILENAMES_DEST[$i]} at destination
	  echo ${FILENAMES_DEST[$i]} >> $delete_list
      fi
    
    done
    echo Done scanning for additional files
fi
