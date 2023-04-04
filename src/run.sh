#!/bin/bash
#SBATCH --job-name=test1
#SBATCH --time=00:10:00
#SBATCH --account=def-khalile2
#SBATCH --mail-user=arnaud.deza@mail.utoronto.ca
#SBATCH --mail-type=ALL

module load python
module load mycplex/20.1.0

source cplex_20_Matrix_Mult/bin/activate


python main.py 2 2 2 7
deactivate
