from model.cp_opt import CPOpt, add_cpo_args
from model.cp_sat import add_cpsat_args


from utils import general_multiplication_tensor
from cp_formulation import CP_general

import argparse


def parse_args():
    parser = argparse.ArgumentParser()

     # '''# arguments pertaining to CPLEX CP parameters
    # parser.add_argument('time_limit', type=int)
    # parser.add_argument('seed', type=int)

    # parser.add_argument('valid_ineq', type=bool)
    # parser.add_argument('symmetry',   type=bool)
    # parser.add_argument('inexact_ineq', type=bool)

    # # arguments pertaining logging and solution saving directory
    # # all files (raw log, stats file, npy files for U,V,W) pertaining to the run will be stored in run_directory
    # parser.add_argument('run_directory', type=str)'''

    # arguments pertaining to matrix multiplication case
    parser.add_argument('N', type=int)
    parser.add_argument('M', type=int)
    parser.add_argument('P', type=int)
    parser.add_argument('R', type=int)

    subparsers = parser.add_subparsers(help='CP Solver', dest="solver")
    subparsers.required = True

    parser_cpo = subparsers.add_parser('cpo', help='IBM CP Optimizer')
    add_cpo_args(parser_cpo)

    parser_sat = subparsers.add_parser('sat', help='OR-Tools CP_SAT Solver')
    add_cpsat_args(parser_sat)

    args = parser.parse_args()
    args_dict = vars(args)
    solver_args = {arg[4:]: args_dict[arg] for arg in args_dict if arg.startswith(args.solver)}

    return args, solver_args


if __name__ == "__main__":
    args, solver_args = parse_args()

    if (args.solver == 'cpo'):
        cp_model = CPOpt(args.N, args.M, args.P, args.R)
        cp_model.solver_params(solver_args)
        sol = cp_model.solve(validate=True)

        print(sol)

    else:
        print('OR-Tools CP_SAT Solver not available yet.')
