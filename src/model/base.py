from utils import general_multiplication_tensor, expand_pd

import numpy as np


class CPModelBase:
    def __init__(self, N, M, P, R,
                    valid_ineq=False, symmetry=False, inexact_ineq=False):
        self.N = N
        self.M = M
        self.P = P
        self.R = R
        self.valid_ineq = valid_ineq
        self.symmetry = symmetry
        self.inexact_ineq = inexact_ineq

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
        T_n = general_multiplication_tensor(self.N, self.M, self.P)

        if (T_cp==T_n).all():
            return True
        else:

            return False

    @classmethod
    def from_file(cls, fp):
        raise NotImplementedError

    def to_file(self, fp):
        raise NotImplementedError

