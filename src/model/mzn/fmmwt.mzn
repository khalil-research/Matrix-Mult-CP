int: N;
int: M;
int: P;
int: R;

set of int: dimI = 1..N*M;
set of int: dimJ = 1..M*P;
set of int: dimK = 1..N*P;
set of int: dimR = 1..R;
       
array[dimI, dimJ, dimK] of int: Tlist;

array[dimI, dimR] of var -1 .. 1: u;
array[dimJ, dimR] of var -1 .. 1: v;
array[dimK, dimR] of var -1 .. 1: w;

constraint forall(i in dimI, j in dimJ, k in dimK)(
    sum (r in dimR) (u[i,r] * v[j,r] * w[k,r]) = Tlist[i,j,k]
);

solve satisfy;