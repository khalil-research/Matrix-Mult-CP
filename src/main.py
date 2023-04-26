from model.cp_opt import add_cpo_args
from model.cp_sat import add_cpsat_args

from slurm.cpo_exec import CPO_Executor

from utils import general_multiplication_tensor
from cp_formulation import CP_general

import os
import uuid
import logging
import submitit
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
    parser.add_argument('--output_dir', type=str, default="../logs", help="Output directory base. Logs and solutions go here.")
    parser.add_argument('--n_seeds', type=int, default=1, help="Number of seeds to test in parallel.")
    parser.add_argument('--n_workers', type=int, default=1, help="Number of threads used by the solver.")

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
    subfolder = f"{args.N}_{args.M}_{args.P}_{args.R}_{uuid.uuid4().hex[:8]}"
    args.output_dir = os.path.join(args.output_dir, subfolder)

    if (args.solver == 'sat'):
        print('OR-Tools CP_SAT Solver not available yet.')
        exit(1)


    executor = submitit.AutoExecutor(folder=args.output_dir)

    executor.update_parameters(
        name=f"mat_mult_{args.N}_{args.M}_{args.P}_{args.R}",
        slurm_account="def-khalile2",
        tasks_per_node=args.n_seeds,
        cpus_per_task=args.n_workers,
        timeout_min= 2 * 24 * 60, # 2 days
        # slurm_partition=args.slurm_partition
        # mem_gb=12*args.slurm_ngpus,
        # gpus_per_node=args.slurm_ngpus,
        # nodes=args.slurm_nnodes,
    )

    cpo_exec = CPO_Executor(args, solver_args)
    job = executor.submit(cpo_exec)

    print("Submitted job_id:", job.job_id)
    print("Output folder:", os.path.abspath(args.output_dir))
