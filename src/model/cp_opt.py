from utils import general_multiplication_tensor
from model.base import CPModelBase

from docplex.cp.model import CpoModel



def add_cpo_args(parser):
    parser.add_argument('--log_period', type=int, default=100000, dest="cpo_LogPeriod")
    parser.add_argument('--seed', type=int, default=4, dest="cpo_RandomSeed")
    # parser.add_argument('--verbose', type=int, default=0, dest='cpo_ctx_verbose')
    # parser.add_argument('--verbose', type=int, default=0, dest='cpo_ctx_verbose')

class CPOpt(CPModelBase):

    def _build_model(self):

        ## Define variables
        self.mdl = CpoModel()
        self.U = [[self.mdl.integer_var(-1, 1, name="U" + str(i) + "_" + str(r)) for r in range(self.N * self.M)] for i in range(self.R)]
        self.V = [[self.mdl.integer_var(-1, 1, name="V" + str(j) + "_" + str(r)) for r in range(self.M * self.P)] for j in range(self.R)]
        self.W = [[self.mdl.integer_var(-1, 1, name="W" + str(k) + "_" + str(r)) for r in range(self.N * self.P)] for k in range(self.R)]

        ## Matrix Multiplication as tensor operation
        T = general_multiplication_tensor(self.N, self.M, self.P)
        for i in range(self.N*self.M):
            for j in range(self.M*self.P):
                for k in range(self.N*self.P):
                    self.mdl.add(self.mdl.sum(self.U[r][i]*self.V[r][j]*self.W[r][k] for r in range(self.R)) == T[i][j][k])

        ## Symmetry
        if self.symmetry:

            # 1.1 Permutation Symmetry  ---  Lexicographic Constraint
            for r in range(self.R-1):
                self.mdl.add(self.mdl.strict_lexicographic(self.U[r]+self.V[r], self.U[r+1]+self.V[r+1]))

            # 1.2 Sign Symmetry ---
            for r in range(self.R):
                # constraint one set first index
                self.mdl.add(self.U[r][0]<=0)
                for i in range(1, self.N*self.M):
                    self.mdl.add(self.U[r][i] <= self.mdl.sum(self.mdl.abs(self.U[r][ip]) for ip in range(i)))

                # constraint one set first index
                self.mdl.add(self.W[r][0]<=0)
                for i in range(1, self.N*self.P):
                    self.mdl.add(self.W[r][i] <= self.mdl.sum(self.mdl.abs(self.W[r][ip]) for ip in range(i)))



        ## Valid Inequalities
        if self.valid_ineq:
            for r in range(self.R):
                #  each U^(r) must have at least one non-zero entry
                self.mdl.add(self.mdl.sum(self.mdl.abs(self.U[r][i]) for i in range(len(self.U[r])))>=1)
                #  each V^(r) must have at least one non-zero entry
                self.mdl.add(self.mdl.sum(self.mdl.abs(self.V[r][i]) for i in range(len(self.V[r])))>=1)
                #  each W^(r) must have at least one non-zero entry
                self.mdl.add(self.mdl.sum(self.mdl.abs(self.W[r][i]) for i in range(len(self.W[r])))>=1)


                # Each output must use at least m of the R terms (inner product requires m)
                for k in range(self.N*self.P):
                    self.mdl.add(self.mdl.sum(self.mdl.abs(self.W[r][k]) for r in range(self.R)) >= self.M)
                    # Each pair of outputs differ by at least 2 R terms
                    for kp in range(self.N*self.P):
                        if k!=kp:
                            self.mdl.add(self.mdl.sum(self.mdl.abs(self.W[r][k] - self.W[r][kp]) for r in range(self.R))>=2)

                # Lower bound on the number of active products
                self.mdl.add(self.mdl.sum(self.mdl.sum(self.mdl.abs(self.U[r][i]) for i in range(self.N*self.M)) *
                                            self.mdl.sum(self.mdl.abs(self.V[r][j]) for j in range(self.M*self.P))
                                            for r in range(self.R)) >= self.M * self.N * self.P)

                # 6) Each product of the form $A_{i,j}B_{j,k}$ must appear in at least one of the $R$ terms
                '''for i in range(M*P):
                    for j in range(self.P*self.N):
                        A_col_idx = (i+1) % P #GOOD
                        B_row_idx = math.floor((1.0*j)/self.N)
                        if A_col_idx == B_row_idx:
                            self.mdl.add(self.mdl.sum(self.mdl.abs(self.U[r][i]*self.V[r][j]) for r in range(self.R)) >= 1)'''


        ## Inexact Inqualities
        if self.inexact_ineq:
                pass

    def seed(self, s):
        params = self.mdl.get_parameters()
        params['RandomSeed'] = s
        self.solver_params(params)

    def solver_params(self, args_dict):
        self.mdl.set_parameters(args_dict)


    def solve(self):
        return self.mdl.solve()


