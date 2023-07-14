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
