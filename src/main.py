import numpy as np
import argparse
import os



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # arguments pertaining to matrix multiplication case
    parser.add_argument('N', type=int)
    parser.add_argument('M', type=int)
    parser.add_argument('P', type=int)
    parser.add_argument('R', type=int)
    
    # arguments pertaining to CPLEX CP parameters
    parser.add_argument('time_limit', type=int)
    parser.add_argument('seed', type=int)
    
    parser.add_argument('valid_ineq', type=bool)
    parser.add_argument('symmetry',   type=bool)
    parser.add_argument('inexact_ineq', type=bool)
    
    # arguments pertaining logging and solution saving directory
    # all files (raw log, stats file, npy files for U,V,W) pertaining to the run will be stored in run_directory
    parser.add_argument('run_directory', type=str)
    
    
    
    # Running
    
    
    
    
    
