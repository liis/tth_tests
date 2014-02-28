#!/usr/bin/env python
import re
import os
import sys
sys.path.append('./')
indir = "VHbb_transfer/from_lorenzo/"
#infilelists_filename = indir + "/filelist_double_el_data.txt"
infilelists_filename = indir + "to_run.txt"

lists = open(infilelists_filename, 'r')

while True: # read line by line
    infilelist = lists.readline().strip('\n')
    if not infilelist: break
    if re.search("skip", infilelist) != None: continue
    
    outdir = (infilelist.split("fileList_")[1]).split(".txt")[0]

    print outdir

    scriptname = "submit_" + outdir + ".sh"
    f = open(scriptname, 'w')
    f.write('#!/bin/bash\n\n')
    f.write('\n\n')
    f.write('data_replica.py --from-site T2_IT_Pisa --to-site T2_EE_Estonia ' + indir+"/"+ infilelist + ' /store/user/liis/VHbb_patTuples/' + outdir)
    f.write('\n\n')
    f.close()
    os.system('chmod +x ' + scriptname)

    submit = "qsub -V -cwd -q long.q -N copy_" +outdir+ " "+scriptname 
    print "Submitting..."
    os.system(submit)

print "Finished job submission"
