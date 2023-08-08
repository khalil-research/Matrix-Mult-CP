import json 
import numpy as np

import sys
sys.path.insert(0,'/Users/chang/PhD_workplace/Matrix-Mult-CP/src')

from utils import general_multiplication_tensor

def mzn_data_generator(N,M,P,R):
    data_dict = {}
    data_dict['N'] = N
    data_dict['M'] = M
    data_dict['P'] = P
    data_dict['R'] = R
    T = general_multiplication_tensor(N,M,P)
    data_dict['Tlist'] = T.tolist()

    file_name = f'fmm_{N}_{M}_{P}_{R}.json'

    with open(file_name, "w") as outfile:
        json.dump(data_dict, outfile)

if __name__ == "__main__":
    input_data_list = [[1,1,1,1],
                        [1,1,2,2],
                        [1,2,1,2],
                        [1,1,3,3],
                        [1,3,1,3],
                        [1,2,2,4],
                        [2,1,2,4],
                        [1,2,3,6],
                        [1,3,2,6],
                        [2,1,3,6],
                        [2,2,2,7],
                        [1,3,3,9],
                        [3,1,3,9],
                        [2,2,3,11],
                        [2,3,2,11],
                        [2,2,4,14],
                        [3,3,3,23]]
    for d in input_data_list:
        mzn_data_generator(d[0],d[1],d[2],d[3])