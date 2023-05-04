from utils import general_multiplication_tensor, cyclic_multiplication_tensor
from model.base import CPModelBase

from docplex.cp.model import CpoModel

import numpy as np

def add_cpo_args(parser):
    parser.add_argument('--log_period', type=int, default=10000000, dest="cpo_LogPeriod")
    parser.add_argument('--seed', type=int, default=4, dest="cpo_RandomSeed")
    # parser.add_argument('--verbose', type=int, default=0, dest='cpo_ctx_verbose')
    # parser.add_argument('--verbose', type=int, default=0, dest='cpo_ctx_verbose')

class CPOpt(CPModelBase):

    def _build_model(self):
        if self.cyclic_invar:
            return self._build_cyclic_model()

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

        if not self.min_add and not self.symmetry and not self.valid_ineq and not self.inexact_ineq:
            print("Running the base model")

        ## Minimize Additions: minimizing non-zero terms in the U, V and W matrices (only used for feasible cases)
        if self.min_add:
            print("With minimization objective.")
            self.mdl.add(self.mdl.minimize(self.mdl.sum(self.mdl.abs(self.U[r][i]) for i in range(self.N * self.M) for r in range(self.R)) +
                self.mdl.sum(self.mdl.abs(self.V[r][j]) for j in range(self.M * self.P) for r in range(self.R)) +
                self.mdl.sum(self.mdl.abs(self.W[r][k]) for k in range(self.N * self.P) for r in range(self.R))))

        ## Symmetry
        if self.symmetry:
            print("Using symmetry breaking.")
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
            print("Using valid inequalities.")
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
            K_1, K_2 = self.inex_bounds
            print("Using inexact inequalities.")

            # constraint 1: sum of nonzeroes in U and V must be less than K_1
            for r in range(self.R):
                self.mdl.add(self.mdl.sum(self.mdl.abs(self.U[r][i]) for i in range(len(self.U[r])))
                    + self.mdl.sum(self.mdl.abs(self.V[r][i]) for i in range(len(self.V[r]))) <= K_1)
            # constraint 2:
            for k in range(self.N*self.P):
                self.mdl.add(self.mdl.sum(self.mdl.abs(self.W[r][k]) for r in range(self.R)) <= K_2)


    def _build_cyclic_model(self):
        n = self.N
        if self.N == 2:
            S = 4
        elif self.N == 3:
            S = 4
        elif self.N == 4:
            S = 12
        else:
            print(f"Not supported N={self.N} for cyclic invariant!")
            exit(1)

        T = int((self.R-S)/3)
        T_n = cyclic_multiplication_tensor(self.N)

        self.mdl = CpoModel()
        self.A = [[self.mdl.integer_var(-1, 1, name="A" + str(n) + "_" + str(r)) for r in range(S)] for n in range(n**2)]
        self.B = [[self.mdl.integer_var(-1, 1, name="B" + str(n) + "_" + str(r)) for r in range(T)] for n in range(n**2)]
        self.C = [[self.mdl.integer_var(-1, 1, name="C" + str(n) + "_" + str(r)) for r in range(T)] for n in range(n**2)]
        self.D = [[self.mdl.integer_var(-1, 1, name="D" + str(n) + "_" + str(r)) for r in range(T)] for n in range(n**2)]


        for i in range(n**2):
            for j in range(n**2):
                for k in range(n**2):
                    r_sum = []
                    for r in range(self.R):
                        if r <=S-1:
                            r_sum.append(self.A[i][r]*self.A[j][r]*self.A[k][r])
                        elif r>=S and r<=S-1+T:
                            r_sum.append(self.B[i][r-S]*self.D[j][r-S]*self.C[k][r-S])
                        elif r>S-2+T and r<=S-1+2*T:
                            r_sum.append(self.C[i][r-S-T]*self.B[j][r-S-T]*self.D[k][r-S-T])
                        else:
                            # print(np.shape(self.D), i, r, S, T, r-S-2*T)
                            # print(np.shape(self.C), j, r, S, T, r-S-2*T)
                            # print("------------")
                            r_sum.append(self.D[i][r-S-2*T]*self.C[j][r-S-2*T]*self.B[k][r-S-2*T])

                    self.mdl.add(self.mdl.sum(r_sum) == T_n[i][j][k])

        if not self.min_add and not self.symmetry and not self.valid_ineq and not self.inexact_ineq:
            print("Running the base model")

        if self.inexact_ineq:
            print("Using inexact inequalities.")
            K_1, K_2 = self.inex_bounds
            # constraint # 1:
            for r in range(T):
                self.mdl.add(self.mdl.sum(self.mdl.abs(self.B[i][r]) for i in range(n**2)) + self.mdl.sum(self.mdl.abs(self.D[i][r]) for i in range(n**2)) <= K_1)
                self.mdl.add(self.mdl.sum(self.mdl.abs(self.C[i][r]) for i in range(n**2)) + self.mdl.sum(self.mdl.abs(self.B[i][r]) for i in range(n**2)) <= K_1)
                self.mdl.add(self.mdl.sum(self.mdl.abs(self.D[i][r]) for i in range(n**2)) + self.mdl.sum(self.mdl.abs(self.C[i][r]) for i in range(n**2)) <= K_1)
            for r in range(S):
                self.mdl.add(self.mdl.sum(self.mdl.abs(self.A[i][r]) for i in range(n**2)) + self.mdl.sum(self.mdl.abs(self.A[i][r]) for i in range(n**2)) <= K_1)

            # constraint # 2:

            for i in range(n**2):
                self.mdl.add(self.mdl.sum(self.mdl.abs(self.A[i][r]) for r in range(S)) +
                    self.mdl.sum(self.mdl.abs(self.B[i][r]) for r in range(T)) +
                    self.mdl.sum(self.mdl.abs(self.C[i][r]) for r in range(T)) +
                    self.mdl.sum(self.mdl.abs(self.D[i][r]) for r in range(T)) <= K_2)




        # Valid Inequalities
        # if self.valid_ineq:
        #     print("Using valid inequalities.")
        #     # 1) each U^(r) must have at least one non-zero entry and same for V^(r)
        #     # and 2) each W_{k} must use at least one of the multiplication terms
        #     for r in range(T):
        #         self.mdl.add(self.mdl.sum(self.mdl.abs(self.B[i][r]) for i in range(n**2)) >=1)
        #         self.mdl.add(self.mdl.sum(self.mdl.abs(self.D[i][r]) for i in range(n**2)) >=1)
        #         self.mdl.add(self.mdl.sum(self.mdl.abs(self.C[i][r]) for i in range(n**2)) >=1)
        #     for r in range(S):
        #         self.mdl.add(self.mdl.sum(self.mdl.abs(self.A[i][r]) for i in range(n**2))>=1)


        #     for k in range(n**2):
        #         # 3) Each output must use at least m of the R terms (inner product requires m)
        #         self.mdl.add(self.mdl.sum(self.mdl.abs(self.A[k][r]) for r in range(S)) +
        #             self.mdl.sum(self.mdl.abs(self.B[k][r]) for r in range(T)) +
        #             self.mdl.sum(self.mdl.abs(self.C[k][r]) for r in range(T)) +
        #             self.mdl.sum(self.mdl.abs(self.D[k][r]) for r in range(T))>=n)
        #     # 4) Each pair of outputs differ by at least two R terms
        #     for kp in range(n**2):
        #         if k != kp:
        #             self.mdl.add(self.mdl.sum(self.mdl.abs(self.A[k][r] - self.A[kp][r]) for r in range(S))
        #                 + self.mdl.sum(self.mdl.abs(self.C[k][r] - self.C[kp][r]) for r in range(T))
        #                 + self.mdl.sum(self.mdl.abs(self.D[k][r] - self.D[kp][r]) for r in range(T))
        #                 + self.mdl.sum(self.mdl.abs(self.B[k][r] - self.B[kp][r]) for r in range(T))>= 2)
        #     # 5) Lower bound on the number of active products

        #     self.mdl.add(self.mdl.sum(self.mdl.sum(self.mdl.abs(self.A[i][r]) for i in range(n**2)) * self.mdl.sum(self.mdl.abs(self.A[i][r]) for i in range(n**2)) for r in range(S)) +
        #         self.mdl.sum(self.mdl.sum(self.mdl.abs(self.B[i][r]) for i in range(n**2)) * self.mdl.sum(self.mdl.abs(self.D[i][r]) for i in range(n**2)) for r in range(T)) +
        #         self.mdl.sum(self.mdl.sum(self.mdl.abs(self.C[i][r]) for i in range(n**2)) * self.mdl.sum(self.mdl.abs(self.B[i][r]) for i in range(n**2)) for r in range(T)) +
        #         self.mdl.sum(self.mdl.sum(self.mdl.abs(self.D[i][r]) for i in range(n**2)) * self.mdl.sum(self.mdl.abs(self.C[i][r]) for i in range(n**2)) for r in range(T)) >=n*n*n)


    def seed(self, s):
        params = self.mdl.get_parameters()
        params['RandomSeed'] = s
        self.solver_params(params)

    def solver_params(self, args_dict):
        self.mdl.set_parameters(args_dict)


    def solve(self):
        return self.mdl.solve()
