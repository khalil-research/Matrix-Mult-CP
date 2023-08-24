To run the matrix multiplication problem in minizinc, run the following command.

```
minizinc fmmwt.mzn fmm_1_1_2_2.json
```

Data files for all feasible cases from the report up to 3x3x3 R=23 is provided in this folder. To generate other instances, run the following.

```
python mzn_data_generator.py -N -M -P -R -dest
``` 
## Runtime results for various solvers through MiniZinc
Time limit is set to 600 seconds.

Size (n,m,p) | Rank | Time (gecode) | Time (chuffed) | Time (cbc) | Time (cp) | Time (mip)
--- | --- | --- | --- | --- | --- | --- 
(1,1,1) | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01
(1,1,2) | 2 | 0.00 | 0.00 | 0.20 | 0.00 | 0.22
(1,1,3) | 3 | 0.00 | 0.00 | 2.65 | 0.00 | 2.63
(1,2,1) | 2 | 0.00 | 0.00 | 0.70 | 0.00 | 0.73
(1,2,2) | 4 | 0.09 | 0.02 | 35.14 | 0.02 | 35.33
(1,2,3) | 6 | TIMEOUT | 1.19 | TIMEOUT | 1.143 | TIMEOUT
(1,3,1) | 3 | 0.00 | 0.0 | 2.51 | 0.00 | 2.50
(1,3,2) | 6 | TIMEOUT | 2.09 | TIMEOUT | 2.16 | TIMEOUT
(1,3,3) | 9 | TIMEOUT | TIMEOUT | TIMEOUT | TIMEOUT | TIMEOUT
(2,1,2) | 4 | 1.69 | 0.09 | 4.41 | 0.10 | 4.38
(2,1,3) | 6 | TIMEOUT | 3.08 | TIMEOUT | 3.08 | TIMEOUT
(2,2,2) | 7 | TIMEOUT | TIMEOUT | TIMEOUT | TIMEOUT | TIMEOUT

