#!/bin/bash
#
# Output directory
#SBATCH --output=/data/hpcdata/users/jambyr/logs/tester.%j.%N.out
#SBATCH --chdir=/data/hpcdata/users/jambyr/tester
#SBATCH --mail-type=begin,end,fail,requeue
#SBATCH --mail-user=jambyr@bas.ac.uk
#SBATCH --time=00:05:00
#SBATCH --partition=quick
#SBATCH --nodes=1-2
#SBATCH --job-name=tester
#

NUM=${1:-128}
NP=${2:-8}

module load hpc/mpich/gcc/3.2
source /data/hpcdata/users/jambyr/tester/venv/bin/activate

mpirun -np $NP python /data/hpcdata/users/jambyr/tester/node_counter.py $NUM

