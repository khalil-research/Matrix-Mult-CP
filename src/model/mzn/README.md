To run the matrix multiplication problem in minizinc, run the following command.

```
minizinc fmmwt.mzn fmm_1_1_2_2.json
```

Data files for all feasible cases from the report up to 3x3x3 R=23 is provided in this folder. To generate other instances, run the following.

```
python mzn_data_generator.py -N -M -P -R -dest
``` 
