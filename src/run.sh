#!/bin/bash
#SBATCH --job-name=test1
#SBATCH --time=10:00:00
#SBATCH --account=def-khalile2
#SBATCH --mail-user=changy.liu@mail.utoronto.ca
#SBATCH --mail-type=ALL

echo "Running on Graham cluster"

module load python
module load mycplex/20.1.0

source /home/liucha90/venvs/bin/activate


python main.py 4 2 2 4 14 cpo-penalty-opt > cpo-penalty-opt_2_2_4_14.txt
# deactivate
