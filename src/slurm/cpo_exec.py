from slurm.base import SLURM_Executor
from model.cp_opt import CPOpt

import os
import random

from submitit.core import plugins


class CPO_Executor(SLURM_Executor):
    def __init__(self, args, solver_args):
        super().__init__(args, solver_args)

        self.cp_model = CPOpt(args.N, args.M, args.P, args.R)
        solver_args["Workers"] = args.n_workers
        self.cp_model.solver_params(solver_args)


    def __call__(self):
        if (self.args.n_seeds > 1):
            self.cp_model.seed(random.randint(0, 9999))

        sol = self.cp_model.solve()
        print(sol.get_solve_status())

        # A hack coz os.getenv("SLURM_JOB_ID") & os.getenv("SLURM_ARRAY_TASK_ID") return None
        # Apparently only
        job_env = plugins.get_job_environment()
        self.job_id  = job_env.job_id
        self.task_id = job_env.global_rank

        if sol:
            if self.cp_model.validate(sol):
                print("Model is valid")
            else:
                print("Model is invalid")

            fname = 'local_solution.txt'

            if self.job_id and self.task_id != None:
                fname = f"{self.job_id}_{self.task_id}_solution.txt"
            sol_f = os.path.join(self.output_dir, fname)
            print(f"Saving solution to: {os.path.abspath(sol_f)}")
            sol.write(sol_f)
