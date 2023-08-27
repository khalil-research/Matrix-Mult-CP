import json 
import numpy as np
import argparse

import sys
sys.path.insert(0,'../src')

from utils import general_multiplication_tensor

def mzn_data_generator(N,M,P,R,dest):
    data_dict = {}
    data_dict['N'] = N
    data_dict['M'] = M
    data_dict['P'] = P
    data_dict['R'] = R
    T = general_multiplication_tensor(N,M,P)
    data_dict['Tlist'] = T.tolist()

    file_name = f'fmm_{N}_{M}_{P}_{R}.json'
    file_location = dest+'/'+file_name

    with open(file_location, "w") as outfile:
        json.dump(data_dict, outfile)

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-N", "--N", default=1, type=int, help="N")
    parser.add_argument("-M", "--M", default=1, type=int, help="M")
    parser.add_argument("-P", "--P", default=1, type=int, help="P")
    parser.add_argument("-R", "--R", default=1, type=int, help="R")
    parser.add_argument("-dest", "--dest", help="datafile destination location")
    args = vars(parser.parse_args())

    mzn_data_generator(args['N'],args['M'],args['P'],args['R'], args['dest'])
