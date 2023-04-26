class SLURM_Executor(object):
    def __init__(self, args, solver_args):
        self.args = args
        self.solver_args = solver_args
        self.output_dir = args.output_dir

    def __call__(self):
        raise NotImplementedError

