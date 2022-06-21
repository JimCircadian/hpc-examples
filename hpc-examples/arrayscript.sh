#!/usr/bin/bash

sleep `expr $1 / 2`
echo "${SLURM_JOB_ID}-`expr ${SLURM_ARRAY_TASK_ID} \* ${SLURM_NTASKS_PER_NODE} \+ ${SLURM_PROCID}` running on `hostname`"
sleep `expr $1 / 2`
#env | grep -i slurm | sort

