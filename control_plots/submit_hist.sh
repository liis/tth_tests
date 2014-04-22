#!/bin/bash

EMERGENCY=true

#qsub run_hist_production.sh SL "--notopw --outdir='./histogrmas/'"
#qsub run_hist_production.sh DL "--notopw --outdir='./histograms/'"

if [  $EMERGENCY == true ]; then
    qsub -q prio run_hist_production.sh SL "--outdir='./histograms/'"
    qsub -q prio run_hist_production.sh DL "--outdir='./histograms/'"
else
    qsub run_hist_production.sh SL "--outdir='./histograms/'"
    qsub run_hist_production.sh DL "--outdir='./histograms/'"
fi

#sh run_hist_production.sh SL " --outdir='./histograms/'"