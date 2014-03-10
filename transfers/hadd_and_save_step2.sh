#! /bin/sh

###############################
# hadd the root-files, produced by VHbb submitStep2.py to have one flat tree per dataset
# Specify INDIR -- directory of root files to hadd
#         OUTDIR -- directory of merged root files
# Optionally set CLEAN_UP=1 to remove input files to hadd on the go
#                COPY_TO_STORAGE=1 to copy trees from /home/ directory to storage element -- note that copying is slow.
###############################

if [ -z $ROOTSYS ]; then
 echo "ROOTSYS is not defined: source ROOT, or hadd won't work!"
 exit
fi

CLEAN_UP=0
COPY_TO_STORAGE=1
OVERWRITE_FILES_AT_STORAGE=0 # set different from 0, if you want to overwrite existing files at storage element

INDIR="Ntuples_new"
OUTDIR_LOCAL="Ntuples_new/Ntuples_merged"

OUTDIR_STORAGE="/hdfs/cms/store/user/liis/TTH_Ntuples_v3/"
SRMPATH="srm://ganymede.hep.kbfi.ee:8888/srm/v2/server?SFN="

BASE_STR="DiJetPt_"
DATASETS=("WZ_TuneZ2star_8TeV_pythia6_tauola" "ZZ_TuneZ2star_8TeV_pythia6_tauola" "WW_TuneZ2star_8TeV_pythia6_tauola" "WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball" "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola" "Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola" "Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola" "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola" "T_s-channel_TuneZ2star_8TeV-powheg-tauola" "T_t-channel_TuneZ2star_8TeV-powheg-tauola" "TTJets_FullLeptMGDecays_8TeV-madgraph" "TTJets_HadronicMGDecays_8TeV-madgraph" "TTJets_MassiveBinDECAY_8TeV-madgraph" "TTJets_SemiLeptMGDecays_8TeV-madgraph" "DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph" "SingleMuRun2012AAug06" "SingleMuRun2012AJul13" "SingleMuRun2012BJul13" "SingleMuRun2012CAug24Rereco" "SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2" "SingleMuRun2012CPromptv2" "SingleMuRun2012CPromptV2TopUp" "SingleMuRun2012D-PromptReco-v1")   

for DATASET in ${DATASETS[@]}
  do
  NR_ROOTFILES=`ls $INDIR"/"*$DATASET*.root 2> /dev/null | wc -l`
  echo Processing dataset $DATASET with $NR_ROOTFILES input files
  
  if [ $NR_ROOTFILES != 0 ]; then
#      hadd -f $OUTDIR_LOCAL"/"$BASE_STR$DATASET.root $INDIR"/"*$DATASET*.root
      if [ $CLEAN_UP == 1 ]; then # clean up the rootfiles
	  echo "Removing initial root files... "
	  rm $INDIR"/"*$DATASET*.root
      fi  
  fi

  if [ $COPY_TO_STORAGE == 1 ] && [ -e $OUTDIR_LOCAL"/"$BASE_STR$DATASET.root ]; then
      echo copying $OUTDIR_LOCAL"/"$BASE_STR$DATASET.root to storage: $OUTDIR_STORAGE

      if [ -e $OUTDIR_STORAGE$BASE_STR$DATASET.root ] && [ $OVERWRITE_FILES_AT_STORAGE == 0 ] ; then
	  echo WARNING! Dataset already exists at destination -- file not copied!
      else
	  srmcp -2 "file:///./"$OUTDIR_LOCAL"/"$BASE_STR$DATASET.root $SRMPATH$OUTDIR_STORAGE$BASE_STR$DATASET.root
	  echo ...done
      fi 
  fi # end if copy to storage

done