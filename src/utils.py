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

<<<<<<< HEAD

def cyclic_multiplication_tensor(N=2):
    """Multiplication tensor.
    The multiplication tensor T of order N is defined by:
        C == A @ B <=> vec(C) == T x1 vec(A.T) x2 vec(B.T)
    where A, B, and C are N x N matrices and vec is the column-wise
    vectorization operator.
    """
    T = np.zeros((N ** 2, N ** 2, N ** 2), dtype=np.int64)
    for n in range(N):
        for m in range(N):
            u = np.ravel_multi_index(
                (n * np.ones(N, dtype=np.int64), np.arange(N)), (N, N))
            v = np.ravel_multi_index(
                (np.arange(N), m * np.ones(N, dtype=np.int64)), (N, N))
            w = np.ravel_multi_index(
                (m, n), (N, N)) * np.ones(len(u), dtype=np.int64)

            T[u, v, w] = 1
    # Assert cyclic symmetry.
    assert np.all(T == np.transpose(T, [2, 0, 1]))
    assert np.all(T == np.transpose(T, [1, 2, 0]))

    return T

=======
>>>>>>> 78285e7fea211b01bfa8214d774d75f81808b2e6
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
