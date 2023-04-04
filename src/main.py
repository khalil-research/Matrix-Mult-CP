from cp_formulation import CP_general
from utils import test_if_U_V_W_is_correct,  general_multiplication_tensor
import argparse

def run(case_):

    R = case_[1]
    N,M,P = case_[0]
    print(R)
    print("\n\n\n\n\n\n")
    print("\n\n\n\n\n\n")
    print("\n\n\n\n\n\n")
    T_n = general_multiplication_tensor(N,M,P)
    print(T_n)

    solution = CP_general(N,M,P,T_n,R,False,False,False,seed = 4)

    if type(solution)!=int:
        is_correct = test_if_U_V_W_is_correct(N,M,P,R,solution,T_n)
        if is_correct:
            print("\n \n Correct low rank decomposition!! \n \n")
        else:
            print("\n \n CP returned SAT but produced incorrect low rank decomposition \n \n")
    else:
        print("Infeasible")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # arguments pertaining to matrix multiplication case
    parser.add_argument('N', type=int)
    parser.add_argument('M', type=int)
    parser.add_argument('P', type=int)
    parser.add_argument('R', type=int)
    
    '''# arguments pertaining to CPLEX CP parameters
    parser.add_argument('time_limit', type=int)
    parser.add_argument('seed', type=int)
    
    parser.add_argument('valid_ineq', type=bool)
    parser.add_argument('symmetry',   type=bool)
    parser.add_argument('inexact_ineq', type=bool)
    
    # arguments pertaining logging and solution saving directory
    # all files (raw log, stats file, npy files for U,V,W) pertaining to the run will be stored in run_directory
    parser.add_argument('run_directory', type=str)'''
    
    args = parser.parse_args()

    case = [ [  args.N,  args.M,   args.P]    ,    args.R  ]
    run(case)
    
   
