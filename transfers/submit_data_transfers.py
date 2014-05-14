#!/usr/bin/env python
import re
import os
import sys
sys.path.append('./')

transfer_ntuples = False
transfer_datasets = True
do_split = False


if transfer_ntuples:
    indir = "Filelists_ntuples/"
else:
    indir = "Filelists_el_track/"

if do_split:
    indir = indir[:-1] + "_split/"
#infilelists_filename = indir + "/filelist_double_el_data.txt"
#indir = "TransfersForResubmit_el_split/"

infilelists_filename = indir + "to_run.txt"
lists = open(infilelists_filename, 'r')

os.system("voms-proxy-init -voms cms")
while True: # read line by line
    infilelist = lists.readline().strip('\n')
    if not infilelist: break
    if re.search("skip", infilelist) != None: continue

    if do_split:
        outdir = infilelist.split("_part_")[0]
        ext = (infilelist.split("_part_")[1]).split(".txt")[0]
    else:
        outdir = infilelist.split(".txt")[0]
        ext = ""
        
#    outdir = (infilelist.split("fail_list_")[1]).split(".txt")[0]
#    outdir = (infilelist.split("fail_list_")[1]).split("_part_")[0]


    print "Saving output to directory: " + outdir

    scriptname = "submit_" + outdir + ext + ".sh" #save unique scriptname
    f = open(scriptname, 'w')
    f.write('#!/bin/bash\n\n')
    f.write('\n\n')
    if transfer_ntuples:
         f.write('data_replica.py --delete --from-site T2_EE_Estonia --to-site T3_CH_PSI ' + indir+"/"+ infilelist + ' /store/user/liis/TTH_Ntuples_allHadTrig')
    elif transfer_datasets:
        f.write('data_replica.py --discovery --to-site T2_EE_Estonia ' + indir+"/"+infilelist + ' /store/user/liis/El_GSF_studies/' + outdir)
    else:
        f.write('data_replica.py --delete --from-site T2_IT_Pisa --to-site T2_EE_Estonia ' + indir+"/"+ infilelist + ' /store/user/liis/VHbb_patTuples/' + outdir)
        #    f.write('data_replica.py --delete --from-site T3_CH_PSI --to-site T2_EE_Estonia ' + indir+"/"+ infilelist + ' /store/user/liis/VHbb_patTuples/' + outdir)
       
    
    f.write('\n\n')
    f.close()
    os.system('chmod +x ' + scriptname)

#    submit = "qsub -V -cwd -q long.q -N copy_" +outdir+ " "+scriptname 
    submit = "qsub -V -cwd -q all.q -N copy_" +outdir+ " "+scriptname
    #    submit = "qsub -N copy_" +outdir+ " "+scriptname 
    print "Submitting... " + submit
    
    os.system(submit)

print "Finished job submission"
