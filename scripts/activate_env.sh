#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/env.config"

module load python/$PYTHON_VER
module load mycplex/$CPLEX_VER

source $VENV_HOME/bin/activate
