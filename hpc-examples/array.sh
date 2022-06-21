#!/bin/bash
#
# Output directory
#SBATCH --output=/data/hpcdata/users/jambyr/tester/multi.%j.%N.out
#SBATCH --chdir=/data/hpcdata/users/jambyr/tester
#SBATCH --mail-type=begin,end,fail,requeue
#SBATCH --mail-user=jambyr@bas.ac.uk
#SBATCH --time=00:05:00
#SBATCH --partition=short
#SBATCH --array=[0-3]
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1
#SBATCH --job-name=arraytest

echo "START `date +%T`"
srun --hint=nomultithread --distribution=block:block -- /data/hpcdata/users/jambyr/tester/arrayscript.sh 10
echo "END `date +%T`"

