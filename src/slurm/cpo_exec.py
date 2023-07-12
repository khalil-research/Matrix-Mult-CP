from slurm.base import SLURM_Executor
from model.cp_opt import CPOpt

import os
import random
import pandas as pd

from submitit.core import plugins


class CPO_Executor(SLURM_Executor):
    def __init__(self, args, solver_args):
        super().__init__(args, solver_args)

        self.cp_model = CPOpt(args.N, args.M, args.P, args.R,
                            cyclic_invar = args.cyclic_invar, min_add = args.min_add,
                            inex_bounds=args.inex_bounds, valid_ineq=args.valid_ineq,
                            symmetry=args.symmetry, inexact_ineq=args.inexact_ineq)

        solver_args["Workers"] = args.n_workers
        solver_args["TimeLimit"] = args.timeout * 60

        if self.args.min_add:
            solver_args["SolutionLimit"] = 1

        self.cp_model.solver_params(solver_args)


    def __call__(self):
        print("Running with:", self.args)
        print("Running solver with:", self.solver_args)

        if (self.args.n_seeds > 1):
            self.cp_model.seed(random.randint(0, 9999))

        sol = self.cp_model.solve()
        print(sol.get_solve_status())

        # A hack coz os.getenv("SLURM_JOB_ID") & os.getenv("SLURM_ARRAY_TASK_ID") return None
        # Also apparently only after the __call__ method is called the resources are allocated and a
        # task_id assigned. That's why we can't have this in the __init__
        job_env = plugins.get_job_environment()
        self.job_id  = job_env.job_id
        self.task_id = job_env.global_rank

        fname = 'local'
        if self.job_id and self.task_id != None:
            fname = f"{self.job_id}_{self.task_id}"

        if sol:
            if self.cp_model.validate(sol):
                print("Model is valid")
            else:
                print("Model is invalid")

            sol_f = os.path.join(self.output_dir, f"{fname}_solution.txt")
            print(f"Saving solution to: {os.path.abspath(sol_f)}")
            sol.write(sol_f)


        sol_f = os.path.join(self.output_dir, f"{fname}_stats.csv")
        print(f"Saving stats to: {os.path.abspath(sol_f)}")
        stats = {
            'N': self.args.N,
            'M': self.args.M,
            'P': self.args.P,
            'R': self.args.R,
            'validineq': self.args.valid_ineq,
            'symmetry': self.args.symmetry,
            'min_add': self.args.min_add,
            'inexactineq': self.args.inexact_ineq,
            'status': sol.get_solve_status(),
            'stime': sol.get_infos().get_solve_time(),
            'ttime': sol.get_infos().get_total_time(),
            'mem': sol.get_infos().get_memory_usage(),
            'numfail': sol.get_infos().get_number_of_fails(),
            'numbranch': sol.get_infos().get_number_of_branches()
            }
        df = pd.DataFrame.from_dict([stats])
        df.to_csv(sol_f)
