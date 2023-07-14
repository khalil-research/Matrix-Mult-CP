#!/bin/bash
#SBATCH --job-name=test1
#SBATCH --time=00:10:00
#SBATCH --account=YOU_SLURM_ACCOUNT

# module load python
# module load mycplex/20.1.0

# source cplex_20_Matrix_Mult/bin/activate


python main.py 2 2 2 7 cpo-penalty-opt
# deactivate
