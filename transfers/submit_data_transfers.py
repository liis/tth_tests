#!/usr/bin/env python
import re
import os
import sys
sys.path.append('./')
#indir = "TransfersForResubmit_split/"
indir = "Filelists_data_el_split/"
#infilelists_filename = indir + "/filelist_double_el_data.txt"

infilelists_filename = indir + "to_run.txt"
lists = open(infilelists_filename, 'r')

os.system("voms-proxy-init -voms cms")
while True: # read line by line
    infilelist = lists.readline().strip('\n')
    if not infilelist: break
    if re.search("skip", infilelist) != None: continue

<<<<<<< HEAD
    outdir = infilelist.split("_part_")[0]
    ext =  (infilelist.split("_part_")[1]).split(".txt")[0]
=======
<<<<<<< HEAD
    outdir = infilelist.split("_part_")[0]
    ext = (infilelist.split("_part_")[1]).split(".txt")[0]
=======
#    outdir = infilelist.split("_part_")[0]
>>>>>>> a76e64700abcd9e5ce8f573a6b457c42a35dbc3d
>>>>>>> 388fbc5e66b41ac23fb20452b980fb3d4d379eb4
#    outdir = infilelist.split(".txt")[0]
#    outdir = (infilelist.split("fileList_")[1]).split(".txt")[0]
#    outdir = (infilelist.split("fail_list_")[1]).split(".txt")[0]
#    outdir = (infilelist.split("fail_list_")[1]).split("_part_")[0]

    print "Saving output to directory: " + outdir

<<<<<<< HEAD
    scriptname = "submit_" + outdir + ext + ".sh" #save unique scriptname
=======
    scriptname = "submit_" + outdir + ext + ".sh"
>>>>>>> 388fbc5e66b41ac23fb20452b980fb3d4d379eb4
    f = open(scriptname, 'w')
    f.write('#!/bin/bash\n\n')
    f.write('\n\n')
    #f.write('data_replica.py --delete --from-site T2_IT_Pisa --to-site T2_EE_Estonia ' + indir+"/"+ infilelist + ' /store/user/liis/VHbb_patTuples/' + outdir)
    
    f.write('python data_replica.py --delete --from-site T2_IT_Pisa --to-site T2_EE_Estonia ' + indir+"/"+ infilelist + ' /store/user/liis/VHbb_patTuples/' + outdir)
    f.write('\n\n')
    f.close()
    os.system('chmod +x ' + scriptname)

#    submit = "qsub -V -cwd -q long.q -N copy_" +outdir+ " "+scriptname 
#    submit = "qsub -V -cwd -q all.q -N copy_" +outdir+ " "+scriptname
    submit = "qsub -N copy_" +outdir+ " "+scriptname 
    print "Submitting... " + submit
    
    os.system(submit)

print "Finished job submission"
