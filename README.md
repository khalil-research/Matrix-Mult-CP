# Matrix Multiplication using Constraint Programming

## Environment Setup
1. Follow [this](https://docs.alliancecan.ca/wiki/CPLEX/en) to download and install the proper CPLEX version.
2. Edit `scripts/env.config` according to your environment.
3. `source scripts/create_env.sh` to create the VENV environment.

## Running the Code
1. Activate the VENV: `source scripts/activate_env.sh`.
2. Run `python src/main.py N M P R {cpo,sat}`. You can specify the solver `cpo` vs `sat` and pass solver specific args.
    - e.g.: `python src/main.py 2 2 2 7 cpo --seed 5`


Look in experiments/readme.md to understand how to run experiments from paper
