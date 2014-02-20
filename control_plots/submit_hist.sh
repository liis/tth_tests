#!/bin/bash

qsub run_hist_production.sh SL "--notrig --notopw"
qsub run_hist_production.sh DL "--notrig --notopw"

qsub run_hist_production.sh SL "--notopw"
qsub run_hist_production.sh DL "--notopw"

qsub run_hist_production.sh SL
qsub run_hist_production.sh DL 