#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/env.config"

module load python/$PYTHON_VER
module load mycplex/$CPLEX_VER

virtualenv --no-download $VENV_HOME
source $VENV_HOME/bin/activate

pip install numpy==1.23.0 --no-index
pip install docplex --no-index
<<<<<<< HEAD
pip install submitit --no-index
pip install scipy --no-index
=======
>>>>>>> 78285e7fea211b01bfa8214d774d75f81808b2e6

python $STUDIO_ROOT/python/setup.py install

