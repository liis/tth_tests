#!/bin/bash

INIT_SRMPATH="srm://stormfe1.pi.infn.it:8444/srm/managerv2?SFN=/cms" # initial location of copied files
INFILELIST="VHbb_transfer/fileList_SingleElectronRun2012AAug06EdmV42.txt" #filelist with input filenames (including full paths)

DEST_SRMPATH="srm://ganymede.hep.kbfi.ee:8888/srm/v2/server?SFN="
DEST_PATH="/hdfs/cms/store/user/liis/VHbb_patTuples/"


#OUTDIR=$1 #later take from an argument
OUTDIR="SingleElectronRun2012AAug06EdmV42/" #defined by INFILELIST name


echo Getting file-lists from final directory: $DEST_SRMPATH$DEST_PATH$OUTDIR
FILENAMES_DEST=(`srmls -l %s $DEST_SRMPATH$DEST_PATH$OUTDIR | awk '{print $2}'`) #Get first/2nd part of the output
FILESIZES_DEST=(`srmls -l %s $DEST_SRMPATH$DEST_PATH$OUTDIR | awk '{print $1}'`) # put parentheses to indicate an array
FILESIZES_DEST=("${FILESIZES_DEST[@]:1}") # remove the first element (name of directory)

NR_FILESIZES_DEST=${#FILESIZES_DEST[@]} #get nr of files
NR_FILENAMES_DEST=${#FILENAMES_DEST[@]}
if [ $NR_FILESIZES_DEST != $NR_FILENAMES_DEST ]; then # sanity chech
    echo WARNING nrFilenames = $NR_FILENAMES_DEST , nrFilesizes = $NR_FILESIZES_DEST -- dont match!
fi


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

    if [ $FILE_DEST == $FILE_INIT ]; then
	MATCH_INIT_DEST=1
	if [ $SIZE_DEST == $SIZE_INIT ]; then
	    SIZE_INIT_DEST=1
	fi
    fi
  done

  if [ $MATCH_INIT_DEST ]; then #Check whether the file exists at destination
      echo Match found
      if [ $SIZE_INIT_DEST ]; then
	  echo With correct size
      else
	  echo "Size init = $SIZE_INIT, size dest = $SIZE_DEST --> Clean up and resubmit copy!"
      fi
  else
      echo No match found --> resubmit copy!
  fi

done < $INFILELIST # done reading initial files from filelist

#for FILENAME in ${FILENAMES_DEST[@]}
#do
#  echo `basename $FILENAME`
#done

#echo ${FILENAMES_DEST[0]}
#echo `basename ${FILENAMES_DEST[0]}`


#echo Matching to $NR_FILESIZES_DEST files at destination






#echo ${FILESIZES_DEST[5]}



#echo ${#FILESIZES_DEST[@]}
#FILENAMES_DEST= $FILENAMES_DEST

#a=(1 2 3)
#echo ${#a[@]} 



#echo $FILESIZES_DEST

#i = 0
#FILESIZES_DEST_LIST=
#for INFILESIZE in $FILENAMES_DEST:
#do
#  echo i = $i
#  echo infilesize = $INFILESIZE
#  
#  FILESIZES_DEST_LIST=(${FILESIZES_DEST_LIST[@]} $i)
#  let i++
#done

#echo $FILESIZES_DEST_LIST

#echo "filenames =" $FILENAMES
#echo "size of filenames = " ${#FILENAMES[*]}
#echo "filesizes =" $FILESIZES
#Filesizes=

#for INFILE_DEST in `srmls $DEST_SRMPATH$DEST_PATH$OUTDIR`
#do
#  echo $INFILE_DEST
#  echo $INFILE_DEST
#  echo -----------------------

 
  # echo `$INFILE_DEST | awk '{print $1}'`


   # echo $INFILE_DEST
#done

#"/hdfs/cms/store/user/liis/VHbb_patTuples/" #backup working testpath for EE

#SIZE_FINAL=`srmls -l %s $DEST_SRMPATH"/store/user/liis/VHbb_patTuples/SingleElectronRun2012AAug06EdmV42/PAT.edm_9_1_5if.root" `

#i=1
#for INFILE_DEST in $FILENAMES_DEST
#do
#  echo $INFILE_DEST
#  echo ${INFILESIZES_DEST[i]}

#  SIZE_INIT=`srmls $INIT_SRMPATH$INFILE_INIT | awk '{print $1}'`
#  echo size init = $SIZE_INIT

#  echo  `srmls $DEST_SRMPATH"/store/user/liis/VHbb_patTuples/SingleElectronRun2012AAug06EdmV42/"`

#  
#  do
#    echo $DEST_SRMPATH$INFILE_DEST
#
#  done

#  SIZE_INIT=`srmls -l %s $INIT_SRMPATH$INFILE" | awk '{print $1}'`
  
#done


#INIT_DIR="/store/user/lpchbb/dlopes/SingleElectronRun2012AAug06EdmV42/dlopes/SingleElectron/HBB_EDMNtupleV42/5acd311e7ac1c2e546a3f05006d77347//"
#FINAL_DIR="/store/user/liis/VHbb_patTuples/"+$OUTDIR



#SIZE_FINAL=`srmls -l %s $FINAL_SRMPATH"/store/user/liis/VHbb_patTuples/SingleElectronRun2012AAug06EdmV42/PAT.edm_9_1_5if.root" | awk '{print $1}'`


#if [ "$SIZE_INIT" != "$SIZE_COPIED" ]; then
#    echo problem with file transfer -- reinitialize transfer! 
#    
#fi