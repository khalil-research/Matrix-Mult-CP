from cp_formulation import CP_general
from utils import test_if_U_V_W_is_correct,  general_multiplication_tensor



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

case = [ [2,2,2]    ,    7]
run(case)

    
    
    
    
    
