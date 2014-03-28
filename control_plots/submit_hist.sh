#!/bin/bash

#qsub run_hist_production.sh SL "--notopw --outdir='./histogrmas/'"
#qsub run_hist_production.sh DL "--notopw --outdir='./histograms/'"


qsub run_hist_production.sh SL "--outdir='./histograms/'"
qsub run_hist_production.sh DL "--outdir='./histograms/'"

#sh run_hist_production.sh SL " --outdir='./histograms/'"