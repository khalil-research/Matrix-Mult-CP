from model.cp_opt import CPOpt, add_cpo_args
from model.cp_penalty_opt import CPPenaltyOpt, add_cpo_penalty_args
from model.cp_sat import add_cpsat_args

from slurm.cpo_exec import CPO_Executor

from utils import general_multiplication_tensor
# from cp_formulation import CP_general

import os
import uuid
import logging
import submitit
import argparse
from datetime import datetime
import calendar

from datetime import datetime

# import sys
# log_file_name = '/home/liucha90/workplace/Matrix-Mult-CP/cp_penalty_opt' + str(datetime.now()) + '.txt'
# f = open(log_file_name, 'w')
# sys.stdout = f

def parse_args():
    parser = argparse.ArgumentParser()

    # arguments pertaining to matrix multiplication case
    parser.add_argument('N', type=int)
    parser.add_argument('M', type=int)
    parser.add_argument('P', type=int)
    parser.add_argument('R', type=int)

    parser.add_argument('--valid_ineq', action='store_true', help="Include valid equalities in the CP model.")
    parser.add_argument('--no-valid_ineq', dest='valid_ineq', action='store_false')
    parser.set_defaults(valid_ineq=False)

    parser.add_argument('--symmetry', action='store_true', help="Include symmetry breaking constrains in the CP model.")
    parser.add_argument('--no-symmetry', dest='symmetry', action='store_false')
    parser.set_defaults(symmetry=False)

    parser.add_argument('--min_add', action='store_true', help="Include an objective to the CP model to minimize the number of additions in the resulting algorithm.")
    parser.add_argument('--no-min_add', dest='min_add', action='store_false')
    parser.set_defaults(min_add=False)

    parser.add_argument('--cyclic_invar', action='store_true', help="Include cyclic invariances (For square x square multiplication only).")
    parser.add_argument('--no-cyclic_invar', dest='cyclic_invar', action='store_false')
    parser.set_defaults(cyclic_invar=False)

    parser.add_argument('--inexact_ineq',
        nargs=2,
        metavar=('K_1', 'K_2'),
        default=(0, 0),
        dest="inex_bounds",
        type=int,
        help="Include inexact inequalitites to cut down the search space (potential incomplete search).")

    parser.add_argument('--output_dir', type=str, default="../logs", help="Output directory base. Logs and solutions go here.")
    parser.add_argument('--n_seeds', type=int, default=1, help="Number of seeds to test in parallel.")
    parser.add_argument('--n_workers', type=int, default=1, help="Number of threads used by the solver.")
    parser.add_argument('--timeout', type=int, default=10, help="Timeout for the run in minutes. (Default: 10)")


    subparsers = parser.add_subparsers(help='CP Solver', dest="solver")
    subparsers.required = True

    parser_cpo = subparsers.add_parser('cpo', help='IBM CP Optimizer')
    add_cpo_args(parser_cpo)

    parser_sat = subparsers.add_parser('sat', help='OR-Tools CP_SAT Solver')
    add_cpsat_args(parser_sat)

    parser_cpo_penalty_opt = subparsers.add_parser('cpo-penalty-opt', help='IBM CP Optimizer')
    add_cpo_penalty_args(parser_cpo_penalty_opt)

    args = parser.parse_args()
    args_dict = vars(args)
    solver_args = {arg[4:]: args_dict[arg] for arg in args_dict if arg.startswith(args.solver)}

    return args, solver_args


if __name__ == "__main__":
    args, solver_args = parse_args()

    subfolder = f"{args.N}x{args.M}x{args.P}_{args.R}_{calendar.month_abbr[datetime.now().month]}{datetime.today().strftime('%d_%H:%M:%S')}"#_{uuid.uuid4().hex[:8]}"
    args.output_dir = os.path.join(args.output_dir, subfolder)
    if args.inex_bounds[0] > 0 and args.inex_bounds[1] >0:
        args.inexact_ineq = True
    else:
        args.inexact_ineq = False

    if (args.solver == 'sat'):
        print('OR-Tools CP_SAT Solver not available yet.')
        exit(1)

    executor = submitit.AutoExecutor(folder=args.output_dir)

    executor.update_parameters(
        name=f"mult_{args.solver}_{args.N}_{args.M}_{args.P}_{args.R}",
        slurm_account="def-khalile2",
        tasks_per_node=args.n_seeds,
        cpus_per_task=args.n_workers,
        timeout_min= args.timeout + 1, # Giveing solver a minute to terminate gracefully
        mem_gb=15,
        additional_parameters={"mail-user":"changy.liu@mail.utoronto.ca","mail-type":"ALL"},
        # "mail-user"="changy.liu@mail.utoronto.ca",
        # "mail-type"="ALL",
        # slurm_partition=args.slurm_partition
        # gpus_per_node=args.slurm_ngpus,
        # nodes=3 #args.slurm_nnodes,
    )

    cpo_exec = CPO_Executor(args, solver_args)
    job = executor.submit(cpo_exec)

    print("Submitted job_id:", job.job_id)
    print("Output folder:", os.path.abspath(args.output_dir))
