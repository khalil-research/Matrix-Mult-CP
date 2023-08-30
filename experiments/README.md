Experimental Setup:
===================
All tasks are run with 10 seeds (sometimes run twice with 5 seeds due to compute constraints).
For infeasible cases we try with and without valid inequalities and symmetry-breaking constraints (all 4 combinations).
For feasible cases, we use the base CP model.


Feasible:
============
**Exp 1:** Run all feasible cases from the report up to 2x2x3 R=11
```
python main.py 1 1 1 1  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 1 1 2 2  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 1 2 1 2  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 1 1 3 3  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 1 3 1 3  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 1 2 2 4  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 2 1 2 4  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 1 2 3 6  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 1 3 2 6  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 2 1 3 6  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 2 2 2 7  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 1 3 3 9  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 3 1 3 9  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 2 2 3 11 --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
python main.py 2 3 2 11 --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/1 cpo
```


**Exp 2:** Sparsity Constraints & Cyclic Invariance
```
python main.py 2 2 2 7  --n_seeds 5 --n_workers 20 --timeout 120 --cyclic_invar  --inexact_ineq 6 4  --output_dir ../logs/2 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 20 --timeout 2880 --inexact_ineq 11 7  --output_dir ../logs/2 cpo
python main.py 3 3 3 23 --n_seeds 5 --n_workers 20 --timeout 2880 --cyclic_invar --inexact_ineq 9 10 --output_dir ../logs/2 cpo
```


Infeasible:
==============
**Exp 3:** Run 2x2x2 with all R=1, 2, 3, 4, 5, 6 with and without valid inequalities and symmetry breaking.
(Time limit is set to 2 hours and each seed uses 8 workers)
```
python main.py 2 2 2 1 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --symmetry    cpo
python main.py 2 2 2 1 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 1 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 1 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --no-symmetry cpo

python main.py 2 2 2 2 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --symmetry    cpo
python main.py 2 2 2 2 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 2 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 2 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --no-symmetry cpo

python main.py 2 2 2 3 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --symmetry    cpo
python main.py 2 2 2 3 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 3 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 3 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --no-symmetry cpo

python main.py 2 2 2 4 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --symmetry    cpo
python main.py 2 2 2 4 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 4 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 4 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --no-symmetry cpo

python main.py 2 2 2 5 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --symmetry    cpo
python main.py 2 2 2 5 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 5 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 5 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --no-symmetry cpo

python main.py 2 2 2 6 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --symmetry    cpo
python main.py 2 2 2 6 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 6 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 6 --n_seeds 5 --n_workers 8 --timeout 120  --output_dir ../logs/3 --no-valid_ineq --no-symmetry cpo
```
