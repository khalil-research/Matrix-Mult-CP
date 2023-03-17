
import gurobipy as gp
from gurobipy import GRB
import numpy as np


def BLP(n,T,R):
    model = gp.Model()
    model.params.SolutionLimit = 1# = gp.Model()
    U_plus = model.addMVar((n**2,R), vtype=GRB.BINARY , name = "U_ir_plus")
    U_minus = model.addMVar((n**2,R), vtype=GRB.BINARY, name = "U_ir_minus")


    V_plus = model.addMVar((n**2,R), vtype=GRB.BINARY , name = "V_ir_plus")
    V_minus = model.addMVar((n**2,R), vtype=GRB.BINARY, name = "V_ir_minus")

    W_plus = model.addMVar((n**2,R), vtype=GRB.BINARY , name = "W_ir_plus")
    W_minus = model.addMVar((n**2,R), vtype=GRB.BINARY, name = "W_ir_minus")

    z = model.addVars(n**2, n**2,n**2, R,8, vtype=GRB.BINARY, name="z")
   

    for i in range(n**2):
        for j in range(n**2):
            for k in range(n**2):
                    model.addConstr(gp.quicksum(z[i,j,k,r,0] - z[i,j,k,r,1] - z[i,j,k,r,2] + z[i,j,k,r,3] - z[i,j,k,r,4]+ z[i,j,k,r,5] + z[i,j,k,r,6]-z[i,j,k,r,7] for r in range(R))==T[i,j,k])
                    for r in range(R):
                        # term 1
                        model.addConstr(z[i,j,k,r,0]<=W_plus[k,r])
                        model.addConstr(z[i,j,k,r,0]<=U_plus[i,r])
                        model.addConstr(z[i,j,k,r,0]<=V_plus[j,r])
                        model.addConstr(z[i,j,k,r,0]>=W_plus[k,r]+ U_plus[i,r]+V_plus[j,r] - 2)

                        # term 2
                        model.addConstr(z[i,j,k,r,1]<=W_plus[k,r])
                        model.addConstr(z[i,j,k,r,1]<=U_plus[i,r])
                        model.addConstr(z[i,j,k,r,1]<=V_minus[j,r])
                        model.addConstr(z[i,j,k,r,1]>=W_plus[k,r]+ U_plus[i,r]+V_minus[j,r] - 2)

                        # term 3
                        model.addConstr(z[i,j,k,r,2]<=W_plus[k,r])
                        model.addConstr(z[i,j,k,r,2]<=U_minus[i,r])
                        model.addConstr(z[i,j,k,r,2]<=V_plus[j,r])
                        model.addConstr(z[i,j,k,r,2]>=W_plus[k,r]+ U_minus[i,r]+V_plus[j,r] - 2)

                        # term 4
                        model.addConstr(z[i,j,k,r,3]<=W_plus[k,r])
                        model.addConstr(z[i,j,k,r,3]<=U_minus[i,r])
                        model.addConstr(z[i,j,k,r,3]<=V_minus[j,r])
                        model.addConstr(z[i,j,k,r,3]>=W_plus[k,r]+ U_minus[i,r]+V_minus[j,r] - 2)

                        # term 5
                        model.addConstr(z[i,j,k,r,4]<=W_minus[k,r])
                        model.addConstr(z[i,j,k,r,4]<=U_plus[i,r])
                        model.addConstr(z[i,j,k,r,4]<=V_plus[j,r])
                        model.addConstr(z[i,j,k,r,4]>=W_minus[k,r]+ U_plus[i,r]+V_plus[j,r] - 2)

                        # term 6
                        model.addConstr(z[i,j,k,r,5]<=W_minus[k,r])
                        model.addConstr(z[i,j,k,r,5]<=U_plus[i,r])
                        model.addConstr(z[i,j,k,r,5]<=V_minus[j,r])
                        model.addConstr(z[i,j,k,r,5]>=W_minus[k,r]+ U_plus[i,r]+V_minus[j,r] - 2)

                        # term 7
                        model.addConstr(z[i,j,k,r,6]<=W_minus[k,r])
                        model.addConstr(z[i,j,k,r,6]<=U_minus[i,r])
                        model.addConstr(z[i,j,k,r,6]<=V_plus[j,r])
                        model.addConstr(z[i,j,k,r,6]>=W_minus[k,r]+ U_minus[i,r]+V_plus[j,r] - 2)

                        # term 8
                        model.addConstr(z[i,j,k,r,7]<=W_minus[k,r])
                        model.addConstr(z[i,j,k,r,7]<=U_minus[i,r])
                        model.addConstr(z[i,j,k,r,7]<=V_minus[j,r])
                        model.addConstr(z[i,j,k,r,7]>=W_minus[k,r]+ U_minus[i,r]+V_minus[j,r] - 2)

    model.setObjective(gp.quicksum(U_plus[i,r]+U_minus[i,r] for i in range(n**2) for r in range(R))+
                       gp.quicksum(V_plus[i,r]+V_minus[i,r] for i in range(n**2) for r in range(R))+
                       gp.quicksum(W_plus[i,r]+W_minus[i,r] for i in range(n**2) for r in range(R))
                       , GRB.MINIMIZE)
    
    model.update()
    vars = model.getVars()
    
    
    model.optimize()
    
    U_sol = np.zeros((n**2,R))
    V_sol = np.zeros((n**2,R))
    W_sol = np.zeros((n**2,R))

    for i in range(n**2):
        for j in range(R):
            U_sol[i,j] = U_plus[i,j].x - U_minus[i,j].x
            V_sol[i,j] = V_plus[i,j].x - V_minus[i,j].x
            W_sol[i,j] =W_plus[i,j].x - W_minus[i,j].x

    t = np.zeros_like(T)
    for i in range(n**2):
        for j in range(n**2):
            for k in range(n**2):
                for r in range(R):
                    t[i,j,k] += U_sol[i,r]*V_sol[j,r]*W_sol[k,r]
    if (t==T).all():
            print("Holy fuck Binary Linear Program got the same T_n")
    return t


def MIP(n,T,R):

    model = gp.Model()
    model.setParam("NonConvex", 2)

    #         ------------    Instantiate variables   ------------ 
    U = model.addMVar((n**2,R), vtype=GRB.INTEGER ,lb = -1,ub =1, name = "U_ir_")
    V = model.addMVar((n**2,R), vtype=GRB.INTEGER ,lb = -1,ub =1, name = "V_ir_")
    W = model.addMVar((n**2,R), vtype=GRB.INTEGER,lb = -1,ub =1, name = "W_ir_")

    V_W_mult = model.addVars(n**2, n**2, R,lb = -1,ub =1, vtype=GRB.INTEGER, name="Multiplication")

    for i in range(n**2):
        for j in range(n**2):
            for k in range(n**2):
                #model.addConstr(gp.quicksum(U[i,r]*V[j,r]*W[k,r] for r in range(R))==T[i,j,k])
                model.addQConstr(gp.quicksum(U[i,r]* V_W_mult[j,k,r] for r in range(R)), GRB.EQUAL, T[i,j,k], "T_ijk_")
                for r in range(R):
                    model.addQConstr(V_W_mult[j,k,r],GRB.EQUAL,V[j,r]*W[k,r])

    model.setObjective(1, GRB.MINIMIZE)
    model.update()
    model.optimize()
    
    U_sol = np.zeros((n**2,R))
    V_sol = np.zeros((n**2,R))
    W_sol = np.zeros((n**2,R))

    for i in range(n**2):
        for j in range(R):
            U_sol[i,j] = U[i,j].x
            V_sol[i,j] = V[i,j].x
            W_sol[i,j] = W[i,j].x

    t = np.zeros_like(T)
    for i in range(n**2):
        for j in range(n**2):
            for k in range(n**2):
                for r in range(R):
                    t[i,j,k] += U_sol[i,r]*V_sol[j,r]*W_sol[k,r]
    if (t==T).all():
            print("Holy fuck non linear MIP got the same T_n")
    return t
