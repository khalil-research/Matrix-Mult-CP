#!/bin/bash
#SBATCH --job-name=mat_mult
#SBATCH --time=00:10:00
#SBATCH --account=def-khalile2


module load python
module load mycplex/20.1.0

source cplex_20_Matrix_Mult/bin/activate

#pip install --no-index --upgrade pip
#pip install numpy==1.21.2+computecanada

python main.py

deactivate
