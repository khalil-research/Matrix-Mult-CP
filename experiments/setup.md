Experimental Setup:
===============
All tasks are run with 10 seeds (sometimes run twice with 5 seeds due to compute constraints).
For infeasible cases we try with and without valid ineq and symmetry breaking constraints (all 4 combinations).
For feasible cases we use base CP model.


1) [pre_experiment] Run 1-4-8 Workers on all 3 platforms using 2x2x2 R=6 and pick the best platform:

python main.py 2 2 2 6 --n_seeds 1 --n_workers 1 --timeout 60  --valid_ineq --symmetry cpo
python main.py 2 2 2 6 --n_seeds 1 --n_workers 4 --timeout 60  --valid_ineq --symmetry cpo
python main.py 2 2 2 6 --n_seeds 1 --n_workers 8 --timeout 60  --valid_ineq --symmetry cpo

                1           4          8
Narval         1517        756        531
Graham         1419        990        725
CSLab          1561        803        609




Infeasible:
===========
2) Do 2x2x2 with all R=1, 2, 3, 4, 5, 6 with and without valid ineq and symmetry breaking.
(Time limit is set to 2 hours and each seed uses 8 workers)

python main.py 2 2 2 1 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --symmetry    cpo
python main.py 2 2 2 1 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 1 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 1 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --no-symmetry cpo

python main.py 2 2 2 2 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --symmetry    cpo
python main.py 2 2 2 2 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 2 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 2 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --no-symmetry cpo

python main.py 2 2 2 3 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --symmetry    cpo
python main.py 2 2 2 3 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 3 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 3 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --no-symmetry cpo

python main.py 2 2 2 4 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --symmetry    cpo
python main.py 2 2 2 4 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 4 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 4 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --no-symmetry cpo

python main.py 2 2 2 5 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --symmetry    cpo
python main.py 2 2 2 5 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 5 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 5 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --no-symmetry cpo

python main.py 2 2 2 6 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --symmetry    cpo
python main.py 2 2 2 6 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --symmetry    cpo
python main.py 2 2 2 6 --n_seeds 5 --n_workers 8 --timeout 120  --valid_ineq    --no-symmetry cpo
python main.py 2 2 2 6 --n_seeds 5 --n_workers 8 --timeout 120  --no-valid_ineq --no-symmetry cpo



3) For infeasible set: 2x2x3 for R=10, 9, 8, 7
(with the time limit of 2 days (2,880 mins) and 20 workers)
with 22 workers we got OOM
now trying with 5 workers and 30GB memory

python main.py 2 2 3 7  --n_seeds 1 --n_workers 5 --timeout 2880 --valid_ineq --symmetry --output_dir ../logs/3 cpo
python main.py 2 2 3 8  --n_seeds 1 --n_workers 5 --timeout 2880 --valid_ineq --symmetry --output_dir ../logs/3 cpo
python main.py 2 2 3 9  --n_seeds 1 --n_workers 5 --timeout 2880 --valid_ineq --symmetry --output_dir ../logs/3 cpo
python main.py 2 2 3 10 --n_seeds 1 --n_workers 5 --timeout 2880 --valid_ineq --symmetry --output_dir ../logs/3 cpo

Feasible:
=========
4) Run all feasible cases from the report up to 2x2x3 R=11

python main.py 1 1 1 1  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 1 1 2 2  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 1 2 1 2  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 1 1 3 3  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 1 3 1 3  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 1 2 2 4  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 2 1 2 4  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 1 2 3 6  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 1 3 2 6  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 2 1 3 6  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 2 2 2 7  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 1 3 3 9  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 3 1 3 9  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 2 2 3 11 --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 2 3 2 11 --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo


My test (for objective add_min:
python main.py 2 2 2 7  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 2 2 2 7  --n_seeds 5 --n_workers 8 --timeout 120 --min_add --output_dir ../logs/4 cpo

python main.py 2 2 3 11  --n_seeds 5 --n_workers 8 --timeout 120 --output_dir ../logs/4 cpo
python main.py 2 2 3 11  --n_seeds 5 --n_workers 8 --timeout 120 --min_add --output_dir ../logs/4 cpo




[RUN THIS with 5 hours (Maybe run it with the inexact ineq)]:
python main.py 2 2 4 14 --n_seeds 5 --n_workers 8 --timeout 120 --no-valid_ineq --no-symmetry cpo



5) Hard feasible cases (3x3x3 R=23): Run on Graham and Narval.
sum_param= [(N*M + M*P)/3, ]
w_param  = [R/3, ]



6) Cyclic:
python main.py 3 3 3 23 --n_seeds 5 --n_workers 20 --timeout 2880 --cyclic_invar --inexact_ineq 9 10 --output_dir ../logs/5 cpo
python main.py 3 3 3 22 --n_seeds 5 --n_workers 20 --timeout 2880 --cyclic_invar --inexact_ineq 9 10 --output_dir ../logs/5 cpo
python main.py 4 4 4 48 --n_seeds 5 --n_workers 20 --timeout 2880 --cyclic_invar --inexact_ineq 12 17 --output_dir ../logs/5 cpo



python main.py 3 3 3 23 --n_seeds 5 --n_workers 20 --timeout 120 --cyclic_invar --inexact_ineq 9 10 --output_dir ../logs/6 cpo
python main.py 3 3 3 23 --n_seeds 5 --n_workers 20 --timeout 120 --output_dir ../logs/6 cpo


python main.py 2 2 2 7  --n_seeds 5 --n_workers 20 --timeout 120 --cyclic_invar --inexact_ineq 6 4 --output_dir ../logs/6 cpo
python main.py 2 2 2 7  --n_seeds 5 --n_workers 20 --timeout 120 --output_dir ../logs/6 cpo


7) Focus on 2x2x4 R=14

python main.py 2 2 4 14 --n_seeds 5 --n_workers 8 --timeout 300 --inexact_ineq 7  7 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 8 --timeout 300 --inexact_ineq 8  7 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 8 --timeout 300 --inexact_ineq 9  7 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 8 --timeout 300 --inexact_ineq 10 7 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 8 --timeout 300 --inexact_ineq 11 7 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 8 --timeout 300 --inexact_ineq 12 7 --output_dir ../logs/7 cpo

python main.py 2 2 4 14 --n_seeds 5 --n_workers 10 --timeout 300 --inexact_ineq 7  8 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 10 --timeout 300 --inexact_ineq 8  8 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 10 --timeout 300 --inexact_ineq 9  8 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 10 --timeout 300 --inexact_ineq 10 8 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 10 --timeout 300 --inexact_ineq 11 8 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 5 --n_workers 10 --timeout 300 --inexact_ineq 12 8 --output_dir ../logs/7 cpo


>>> Increase the time-limit:
python main.py 2 2 4 14 --n_seeds 10 --n_workers 5 --timeout 5760 --inexact_ineq 7  7 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 10 --n_workers 5 --timeout 5760 --inexact_ineq 8  7 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 10 --n_workers 5 --timeout 5760 --inexact_ineq 9  7 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 10 --n_workers 5 --timeout 5760 --inexact_ineq 10 7 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 10 --n_workers 5 --timeout 5760 --inexact_ineq 11 7 --output_dir ../logs/7 cpo
python main.py 2 2 4 14 --n_seeds 10 --n_workers 5 --timeout 5760 --inexact_ineq 12 7 --output_dir ../logs/7 cpo
