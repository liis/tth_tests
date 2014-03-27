#!/bin/bash

#qsub run_hist_production.sh SL "--notopw --outdir='./histogrmas/'"
#qsub run_hist_production.sh DL "--notopw --outdir='./histograms/'"


#qsub run_hist_production.sh SL "--outdir='./histograms_LRplot/'"
qsub run_hist_production.sh DL "--outdir='./histograms_LRplot/'"

#sh run_hist_production.sh SL " --outdir='./histograms/'"