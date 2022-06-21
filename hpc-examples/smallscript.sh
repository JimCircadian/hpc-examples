#!/usr/bin/bash

sleep $1
echo "${SLURM_JOB_ID}-${SLURM_PROCID} running on `hostname`"
sleep $1
#env | grep -i slurm | sort

