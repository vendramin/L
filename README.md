# On the enumeration of finite L-algebras 

[![DOI](https://zenodo.org/badge/417288153.svg)](https://zenodo.org/badge/latestdoi/417288153)

The repository contains database of several finite L-algebras. This is based on the paper  

> C. Dietzel, P. Menchón, L. Vendramin. On the enumeration of finite L-algebras. 

Here is a short description of some of the files. 

The files L.g has methods to construct finite L-algebras. The difference between 
these files is related to the symmetry breaking. 

```
$ gap L.g 
gap> construct_L(4);
Running savilerow. I found 44 solutions
I constructed 44 L-algebras in 3780ms (= 0:00:03.780)
``` 

The difference between L.g and L_partial.g is related to the symmetry breaking. 

```
$ gap L_partial.g 
gap> construct_L(4);
Running savilerow. I found 44 solutions
I constructed 44 L-algebras in 442ms (= 0:00:00.442)
```

The files enumerate_L.g and enumerate_hilbert.g only enumerate structures, the construction is not performed. 

```
$ gap enumerate_L.g 
gap> enumerate_L(4);
Created output file for domain filtering L4.eprime.minion
Created output file L4.eprime.minion
Created information file L4.eprime.info
Running savilerow. There are 44 L-algebras in 435ms (= 0:00:00.435)
```

There are similar files for constructing and enumerating finite Hilbert algebras. 

## L-algebras of size 8

The database of L-algebras of size 8 requires a different approach. We split the calculation into three cases:

* Diamond poset. To enumerate/construct these L-algebras use the Python script `diamond/diamond.py`. The database (for GAP, compressed) is `data/diamond8.tar`.  
* Trivial poset (i.e. discrete L-algebras). To enumerate/construct discrete L-algebras use the Python script `discrete/discrete.py`. The database (GAP, compressed) is `data/discrete8.tar`. 
* Other posets. To enumerate/construct these L-algebras use the Python script `non_discrete/non_discrete.py`. The database (for GAP, compressed) is `data/non_discrete8.tar`. 
