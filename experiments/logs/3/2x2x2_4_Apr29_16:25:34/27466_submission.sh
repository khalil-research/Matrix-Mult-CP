#!/bin/bash

# Parameters
#SBATCH --cpus-per-task=8
#SBATCH --error=/h/30/pashootan/Matrix-Mult-CP/src/../logs/2x2x2_4_Apr29_16:25:34/%j_0_log.err
#SBATCH --job-name=mult_2_2_2_4
#SBATCH --mem=12GB
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --open-mode=append
#SBATCH --output=/h/30/pashootan/Matrix-Mult-CP/src/../logs/2x2x2_4_Apr29_16:25:34/%j_0_log.out
#SBATCH --signal=USR2@90
#SBATCH --time=2881
#SBATCH --wckey=submitit

# command
export SUBMITIT_EXECUTOR=slurm
srun --unbuffered --output /h/30/pashootan/Matrix-Mult-CP/src/../logs/2x2x2_4_Apr29_16:25:34/%j_%t_log.out --error /h/30/pashootan/Matrix-Mult-CP/src/../logs/2x2x2_4_Apr29_16:25:34/%j_%t_log.err /h/30/pashootan/.virtualenvs/matmul/bin/python -u -m submitit.core._submit /h/30/pashootan/Matrix-Mult-CP/src/../logs/2x2x2_4_Apr29_16:25:34
