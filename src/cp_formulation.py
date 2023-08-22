from docplex.cp.model import CpoModel
import numpy as np
import math


def CP_general(N,M,P,T,R,valid_ineq,symmetry,inexact_ineq,seed):
    ## Define variables
    mdl = CpoModel()
    u = [[mdl.integer_var(-1, 1, name="U" + str(i) + "_" + str(r)) for r in range(N*M)] for i in range(R)]
    v = [[mdl.integer_var(-1, 1, name="V" + str(j) + "_" + str(r)) for r in range(M*P)] for j in range(R)]
    w = [[mdl.integer_var(-1, 1, name="W" + str(k) + "_" + str(r)) for r in range(N*P)] for k in range(R)]
    
    ## Matrix Multiplication as tensor operation
    for i in range(N*M):
        for j in range(M*P):
            for k in range(N*P):
                mdl.add(mdl.sum(u[r][i]*v[r][j]*w[r][k] for r in range(R)) == T[i][j][k])
    
    ## Symmetry
    if symmetry:
    
              # 1.1 Permutation Symmetry  ---  Lexicographic Constraint
              for r in range(R-1):       mdl.add(mdl.strict_lexicographic(u[r]+v[r], u[r+1]+v[r+1]))

              # 1.2 Sign Symmetry --- 
              for r in range(R):
                # constraint one set first index 
                mdl.add(u[r][0]<=0)
                for i in range(1, N*M):
                    mdl.add(u[r][i] <= mdl.sum(mdl.abs(u[r][ip]) for ip in range(i)))
                    
                # constraint one set first index 
                mdl.add(w[r][0]<=0)
                for i in range(1, N*P):
                    mdl.add(w[r][i] <= mdl.sum(mdl.abs(w[r][ip]) for ip in range(i)))



    ## Valid Inequalities
    if valid_ineq:
              for r in range(R):
                  #  each U^(r) must have at least one non-zero entry
                  mdl.add(mdl.sum(mdl.abs(u[r][i]) for i in range(len(u[r])))>=1)
                  #  each V^(r) must have at least one non-zero entry
                  mdl.add(mdl.sum(mdl.abs(v[r][i]) for i in range(len(v[r])))>=1)
                  #  each W^(r) must have at least one non-zero entry
                  mdl.add(mdl.sum(mdl.abs(w[r][i]) for i in range(len(w[r])))>=1)


              # Each output must use at least m of the R terms (inner product requires m)
              for k in range(N*P):
                mdl.add(mdl.sum(mdl.abs(w[r][k]) for r in range(R)) >= M)
                # Each pair of outputs differ by at least 2 R terms
                for kp in range(N*P):
                  if k!=kp:
                    mdl.add(mdl.sum(mdl.abs(w[r][k] - w[r][kp]) for r in range(R))>=2)
              # Lower bound on the number of active products
              mdl.add(mdl.sum(mdl.sum(mdl.abs(u[r][i]) for i in range(N*M)) * mdl.sum(mdl.abs(v[r][j]) for j in range(M*P)) for r in range(R)) >= M*N*P)
              # 6) Each product of the form $A_{i,j}B_{j,k}$ must appear in at least one of the $R$ terms  
              '''for i in range(M*P):
                  for j in range(P*N):
                      A_col_idx = (i+1) % P #GOOD
                      B_row_idx = math.floor((1.0*j)/N)
                      if A_col_idx == B_row_idx:
                        mdl.add(mdl.sum(mdl.abs(u[r][i]*v[r][j]) for r in range(R)) >= 1)'''
    ## Inexact Inqualities
    if inexact_ineq:
            pass
    
    mdl.set_parameters({'LogPeriod': 100000,'RandomSeed':seed})
  
    #mdl.set_parameters({'LogVerbosity': 'Quiet'})

    msol = mdl.solve()
    if msol:
      return [msol,u,v,w]
    else:
      print("Infeasible")
      return -1
