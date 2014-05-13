#!/usr/bin/env python
import re
import os
import sys
sys.path.append('./')
indir = "Filelists_mc_additional/"
#indir = "TransfersForResubmit_el/"
#indir = "Filelists_data/"
#infilelists_filename = indir + "/filelist_double_el_data.txt"

infilelists_filename = indir + "to_run.txt"

lists = open(infilelists_filename, 'r')

while True: # read line by line
    infilelist = lists.readline().strip('\n')
    if not infilelist: break
    if re.search("skip", infilelist) != None: continue

    outdir = infilelist.split(".txt")[0]
#    outdir = (infilelist.split("fileList_")[1]).split(".txt")[0]
#    outdir = (infilelist.split("fail_list_")[1]).split(".txt")[0]

    print "Start processing: " + outdir


#    os.system('data_replica.py --delete --from-site T2_IT_Pisa --to-site T2_EE_Estonia ' + indir+"/"+ infilelist + ' /store/user/liis/VHbb_patTuples/' + outdir)
    os.system('data_replica.py --delete --from-site T3_CH_PSI --to-site T2_EE_Estonia ' + indir+"/"+ infilelist + ' /store/user/liis/VHbb_patTuples/' + outdir)


print "Finished filelists"
