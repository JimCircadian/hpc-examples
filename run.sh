#!/bin/bash
#
# Output directory
#SBATCH --output=/data/hpcdata/users/jambyr/logs/job.%j.%N.out
#SBATCH --chdir=/data/hpcdata/users/jambyr/
#SBATCH --mail-type=begin,end,fail,requeue
#SBATCH --mail-user=jambyr@bas.ac.uk
#SBATCH --time=00:05:00
#SBATCH --partition=quick
#SBATCH --nodes=1-2
#
# Load the modules
source /etc/profile.d/modules.sh
module load hpc/python/conda-python-3.6.4

mpirun -np $SLURM_NTASKS $1

