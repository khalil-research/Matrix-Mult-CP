# Matrix Multiplication using Constraint Programming

Overleaf link for symmetry pruning: https://www.overleaf.com/5527138239pnfvrpxzcmfj

To-Do:
- Read and Implement symmetry handling
- Matrix multiplication constraints for specific matrices (diagonal, upper triangular, skew, etc...)
- Parralelization with Compute Canada
- In the case of infeasibility, how to generate a proof

## Table for square matrices

Size (n,m,p) | Best known Rank | Our rank | Time | # branches | # fails 
--- | --- | --- | --- | --- | --- 
(2,2,2) | 7 | 7 | 2.46 | x | x
(3,3,3) | 23 | N/A | N/A | N/A | N/A
(4,4,4) | 47 | N/A | N/A | N/A | N/A
(5,5,5) | 96 | N/A | N/A | N/A | N/A

## Table for square matrices using cyclic invariance constraint
R = S + 3*T

Size (n,m,p) | Best known Rank | Our rank | S | T | Time | # branches | # fails 
--- | --- | --- | --- | --- | --- | --- | ---
(2,2,2) | 7 | 7 | 1 | 2 | 0.14 | 12578 | 6086
(2,2,2) | 7 | 7 | 4 | 1 | 0.62 | 57728 | 28003

## Table for non-square matrices
Size (n,m,p) | Best known Rank | Our rank | Time (seconds) | # branches | # fails
--- | --- | --- | --- | --- | ---
(2,2,3) | 11 | 11 | 122.67 | 8094049 | 3666016
(2,2,4) | 14 | x | 2+ hrs | x | x
(2,2,5) | 18 | N/A | N/A | N/A | N/A
(2,3,3) | 15 | N/A | N/A | N/A | N/A
(2,3,4) | 20 | N/A | N/A | N/A | N/A
(2,3,5) | 25 | N/A | N/A | N/A | N/A
(2,4,4) | 26 | N/A | N/A | N/A | N/A
(3,3,4) | 29 | N/A | N/A | N/A | N/A
