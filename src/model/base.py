from utils import general_multiplication_tensor, cyclic_multiplication_tensor, expand_pd

import numpy as np


class CPModelBase:
    def __init__(self, N, M, P, R,
                    cyclic_invar=False, min_add=False,
                    valid_ineq=False, symmetry=False,
                    inex_bounds=None, inexact_ineq=False):
        self.N = N
        self.M = M
        self.P = P
        self.R = R
        self.min_add = min_add
        self.valid_ineq = valid_ineq
        self.symmetry = symmetry
        self.inex_bounds = inex_bounds
        self.inexact_ineq = inexact_ineq
        self.cyclic_invar = cyclic_invar

        self.U = None
        self.V = None
        self.W = None
        self._mdl = self._build_model()

    def __call__(self):
        return self._mdl

    def _build_model(self):
        raise NotImplementedError

    def solver_params(self, name, val=None):
        raise NotImplementedError

    def seed(self, s):
        raise NotImplementedError

    def solve(self):
        raise NotImplementedError

    def validate(self, sol):
        if self.cyclic_invar:
            if self.N == 2:
                S = 4
            elif self.N == 3:
                S = 5
            else:
                print(f"Not supported N={self.N} for cyclic invariant!")
                exit(1)
            T = int((self.R-S)/3)
            T_n = cyclic_multiplication_tensor(self.N)

            A_sol = np.zeros((self.N**2,S))
            B_sol = np.zeros((self.N**2,T))
            C_sol = np.zeros((self.N**2,T))
            D_sol = np.zeros((self.N**2,T))

            for i in range(self.N**2):
                for r in range(S):
                    A_sol[i,r] = sol[self.A[i][r]]
                for r in range(T):
                    B_sol[i,r] = sol[self.B[i][r]]
                    C_sol[i,r] = sol[self.C[i][r]]
                    D_sol[i,r] = sol[self.D[i][r]]

            U_sol = np.hstack((A_sol, B_sol, C_sol, D_sol))
            V_sol = np.hstack((A_sol, D_sol, B_sol, C_sol))
            W_sol = np.hstack((A_sol, C_sol, D_sol, B_sol))
        else:
            T_n = general_multiplication_tensor(self.N, self.M, self.P)

            U_sol = np.zeros((self.M*self.N,self.R))
            V_sol = np.zeros((self.P*self.M,self.R))
            W_sol = np.zeros((self.P*self.N,self.R))

            for i in range(self.M*self.N):
                for r in range(self.R):
                    U_sol[i,r] = sol[self.U[r][i]]

            for i in range(self.P*self.M):
                for r in range(self.R):
                    V_sol[i,r] = sol[self.V[r][i]]
            for i in range(self.P*self.N):
                for r in range(self.R):
                    W_sol[i,r] = sol[self.W[r][i]]

        T_cp = expand_pd(U_sol, V_sol, W_sol)


        if (T_cp==T_n).all():
            return True
        else:

            return False

    @classmethod
    def from_file(cls, fp):
        raise NotImplementedError

    def to_file(self, fp):
        raise NotImplementedError

