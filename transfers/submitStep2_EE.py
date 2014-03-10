#!/usr/bin/env python

#############
# run at /VHbbAnalysis/VHbbDataFormats/bin
#############

import commands
import re
import os
import string
import FWCore.ParameterSet.Config as cms
import math

import sys
sys.path.append('./')

print "Import cfg file from ntuple.py"
from ntuple  import process 

debug    = False
outdir = './Ntuples_new'
print "Saving output to " + outdir

def processAllBatch(jobName, isPisa, outName, split): #isPisa is a placeholder

    process.fwliteInput.fileNames = ()

    if string.find( jobName, 'Run2012' )>0:
        process.Analyzer.isMC  = cms.bool(False)
    
    input = open('filelists/filelist_'+jobName+'.txt','r')
    counter     = 1
    counterJobs = 0
    for line in input:
        foo = line.strip('\n')
        if counter>=split[0] and counter<=split[1]:
            process.fwliteInput.fileNames.append(foo)
            counterJobs += 1
        counter += 1

    input.close()

    outFileName = outName+'_'+str(split[0])+'-'+str(split[1])+'.root'
    
    process.fwliteOutput.fileName = cms.string(outdir+'/'+outFileName)

    out = open('myStep2_'+jobName+'_'+str(split[0])+'-'+str(split[1])+'.py','w')
    out.write(process.dumpPython())
    out.close()

    scriptName = 'myStep2_'+jobName+'_'+str(split[0])+'-'+str(split[1])+'.sh'
    
    f = open(scriptName,'w')
    f.write('#!/bin/bash\n\n')
    f.write('cd /home/liis/TTH_Ntuples/CMSSW_5_3_3/src/VHbbAnalysis/VHbbDataFormats/bin/\n')#/shome/liis/CMSSW_5_3_3_patch2_New/src/VHbbAnalysis/VHbbDataFormats/bin\n')
    f.write('export SCRAM_ARCH="slc5_amd64_gcc462"\n')
    f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
    f.write('eval `scramv1 runtime -sh`\n')
    f.write('\n')
    f.write('\n')

    mainexec = 'Ntupler myStep2_'+jobName+'_'+str(split[0])+'-'+str(split[1])+'.py'
    print mainexec
    f.write(mainexec+'\n\n')           

#    f.write("srmcp " + outdir + "/" + outFileName + "srm://ganymede.hep.kbfi.ee:8888/srm/v2/server?SFN=/hdfs/cms/store/user/liis/TTH_Ntuples_v3/ \n")
#    f.write("rm " + outdir + "/" + outFileName + "\n" )
            
    f.close()

    os.system('chmod +x '+scriptName)
    submitToQueue = 'qsub -N my'+jobName+'_'+str(split[0])+'-'+str(split[1])+' '+scriptName 

    if not debug:
        os.system(submitToQueue)
        print submitToQueue


    return float(counterJobs)/float(counter-1)

###########################################################################
###########################################################################


files_per_job = 30
#infile_path = "/hdfs/cms/store/user/liis/VHbb_patTuples/"

print "Processing data-samples..."
data_samples = { # dataset_name: nr_of_files
#    "SingleMuRun2012AAug06": 49,
#    "SingleMuRun2012AJul13": 391,
#    "SingleMuRun2012BJul13": 1576,
#    "SingleMuRun2012CAug24Rereco": 196,
#    "SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2": 51,
#    "SingleMuRun2012CPromptv2": 1681, 
#    "SingleMuRun2012CPromptV2TopUp": 577,
#    "SingleMuRun2012D-PromptReco-v1": 1441,
    }

for data_sample in data_samples:
    nr_input_files = data_samples[data_sample]
    nr_jobs = int(math.ceil(float(nr_input_files)/files_per_job))
    print "Submitting " + data_sample + " with " + str(nr_jobs) + " jobs"

    total = 0
    for k in range(nr_jobs):
        print "Processing job nr. ", k
        total += processAllBatch(data_sample, 1, data_sample, [k*files_per_job+1,(k+1)*files_per_job])
    print '**************************************\nFraction of processed sample: %s\n**************************************\n' % total

mc_samples = {
#    "DiJetPt_DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph": 197,
#    "DiJetPt_TTJets_SemiLeptMGDecays_8TeV-madgraph": 1697,
#    "DiJetPt_TTJets_FullLeptMGDecays_8TeV-madgraph": 782,
#    "DiJetPt_TTJets_HadronicMGDecays_8TeV-madgraph": 922,    
#    "DiJetPt_TTJets_MassiveBinDECAY_8TeV-madgraph": 45,
    # FIXME ADD OTHERS
    }

for mc_sample in mc_samples:
    nr_input_files = mc_samples[mc_sample]
    nr_jobs = int(math.ceil(float(nr_input_files)/files_per_job))
    jobname_mc = (mc_sample.split("DiJetPt_")[1]).split("_8TeV")[0]
    print "Submitting " + jobname_mc + " with " + str(nr_jobs) + " jobs"

    total = 0
    for k in range(nr_jobs):
        print "Processing....", k
        total += processAllBatch(jobname_mc, 1, mc_sample, [k*files_per_job  +1,(k+1)*files_per_job ])
        print '\n**************************************\nFraction of processed sample: %s\n**************************************' % total

