#!/bin/bash

# Parameters
#SBATCH --cpus-per-task=8
#SBATCH --error=/h/30/pashootan/Matrix-Mult-CP/src/../logs/4/2x3x2_11_May02_20:04:32/%j_0_log.err
#SBATCH --job-name=mult_2_3_2_11
#SBATCH --mem=12GB
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --open-mode=append
#SBATCH --output=/h/30/pashootan/Matrix-Mult-CP/src/../logs/4/2x3x2_11_May02_20:04:32/%j_0_log.out
#SBATCH --signal=USR2@90
#SBATCH --time=121
#SBATCH --wckey=submitit

# command
export SUBMITIT_EXECUTOR=slurm
srun --unbuffered --output /h/30/pashootan/Matrix-Mult-CP/src/../logs/4/2x3x2_11_May02_20:04:32/%j_%t_log.out --error /h/30/pashootan/Matrix-Mult-CP/src/../logs/4/2x3x2_11_May02_20:04:32/%j_%t_log.err /h/30/pashootan/.virtualenvs/matmul/bin/python -u -m submitit.core._submit /h/30/pashootan/Matrix-Mult-CP/src/../logs/4/2x3x2_11_May02_20:04:32
