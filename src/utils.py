import numpy as np

def general_multiplication_tensor(N, M, P):
   """Multiplication tensor.
   The multiplication tensor T in {0,1} of size NM x MP x PN
   for the multiplication of two matrices of size NxM and MxP
   """
   T = np.zeros((N * M, M * P, N * P), dtype=np.int64)
   for n in range(N):
       for m in range(M):
           for p in range(P):
               # Convert multi-dimensional indices to flat indices.
               a_index = np.ravel_multi_index((n, m), (N, M))
               b_index = np.ravel_multi_index((m, p), (M, P))
               c_index = np.ravel_multi_index((n, p), (N, P))
               T[a_index, b_index, c_index] = 1
   return T

def expand_pd(U, V, W):
    """Expand a polyadic decomposition.
    The polyadic expansion T of the factor matrices U, V, and W is defined by:
        T[i, j, k] = \sum_r U[i, r] * V[j, r] * W[k, r].
    """
    I, J, K, R = U.shape[0], V.shape[0], W.shape[0], U.shape[1]
    T = np.zeros((I, J, K))
    for i in range(I):
        for j in range(J):
            for k in range(K):
                for r in range(R):
                    T[i, j, k] += U[i, r] * V[j, r] * W[k, r]
    return T



def test_if_U_V_W_is_correct(N,M,P,R,solution,T_n):
    ''' Checks if U,V,W found by CP formulation is a true correct low rank decomposition of T_n 
        Returns True if correct else False'''
    sol,U,V,W = solution
    U_sol = np.zeros((M*N,R))
    V_sol = np.zeros((P*M,R))
    W_sol = np.zeros((P*N,R))
    
    for i in range(M*N):
      for r in range(R):        U_sol[i,r] = sol[U[r][i]]
    for i in range(P*M):
      for r in range(R):        V_sol[i,r] = sol[V[r][i]]
    for i in range(P*N):
      for r in range(R):        W_sol[i,r] = sol[W[r][i]]
      
    
    t_constraint_programming = expand_pd(U_sol, V_sol, W_sol)

    if (t_constraint_programming==T_n).all():
      return True
    else:
      return False
