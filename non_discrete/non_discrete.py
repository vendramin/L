import itertools
import math
import sys,os,time,subprocess
import copy

def youngsubgroup(s): # s is a monotonous sequence of integers - this constructs the symmetry group of s
    l = len(s)
    uniques = [s[k] for k in range(l) if ((k==0) or (s[k-1]!=s[k]))]
    n = len(uniques)
    counts = [s.count(u) for u in uniques]
    indices = [0]+list(itertools.accumulate(counts))
    youngfactors = [list(itertools.permutations(range(indices[k],indices[k+1]))) for k in range(n)]

    youngsubgroup = [tuple(itertools.chain(*factors)) for factors in itertools.product(*youngfactors)]

    return(youngsubgroup)

def invdictionary(n): # a dictionary with inverses of permutations - so we need not calculate them every time!
    dict = {}
    for perm in itertools.permutations(range(n)):
        inv = [None]*n
        for k in range(n):
            inv[perm[k]] = k
        dict.update({perm:tuple(inv)})
    return dict

def lextest_aut(upsets,invdict): # given the dictionary of inverses, tests lex_minimality and calculates automorphism groups for lex-minimal posets
    n = len(upsets)
    sig = [len(u) for u in upsets]
    young = youngsubgroup(sig) # the sizes of Upsets aren't altered by an automorphism, so we only need to look in a Young subgroup
    aut = []
    for perm in young:
        inv = invdict[perm]
        for k in range(n):
            M = upsets[inv[k]]
            N = {perm[x] for x in M}


            compare = revlex(upsets[k],N)

            if compare == "le":
                break
            elif compare == "gr":
                return [False]
            elif k+1 == n:
                aut.append(perm)

    return [True,aut]



def revlex(A,B): # orders sets of equal size rev-lexicographically

    if A == B:
        return "eq"
    else:
        gr = max(A.symmetric_difference(B))

        if gr in A:
            return "gr"
        else:
            return "le"

def partial_orders(n):

    P0 = [[{0}],1,[set([]),{0}]] # List of upsets ; size of biggest upset ; filters of the poset
    list_of_posets = [P0]

    for k in range(1,n):

        new_posets = []

        for P in list_of_posets:
            upsets = P[0]
            size_biggest_upset = P[1]
            filters = P[2]


            upsets_for_k = [A.union({k}) for A in filters if len(A) >= size_biggest_upset-1]

            for U in upsets_for_k:

                filters_with_k = []

                for F in filters:
                    newF = F.union(U)
                    if newF not in filters_with_k:
                        filters_with_k.append(newF)

                newfilters = filters + filters_with_k

#                print(newfilters)

                new_posets.append([upsets+[U],len(U),newfilters])


        invdict = invdictionary(k+1)

        if k < n-1:
            new_posets = [P for P in new_posets if lextest_aut(P[0],invdict)[0] == True]
            list_of_posets = new_posets.copy()
        else:
            list_of_posets = [[P[0],lextest_aut(P[0],invdict)[1],P[2]] for P in new_posets if lextest_aut(P[0],invdict)[0] == True]

    return list_of_posets

def poset_binary(P): # P is a list of upsets, but we want a 01-matrix!
    n = len(P)
    L = [[0]*n for k in range(n)]

    for i in range(n):
        for j in P[i]:
            L[i][j] = 1
    return(L)


def squenumerate(n): # gives an explicit enumeration of an nxn-Board

    x = 1
    y = 1

    En = [[x,y]]

    while (x != n or y !=1):
        if x < y:
            x += 1
        elif y != 1:
            y -= 1
        else:
            y = x+1
            x = 1
        En.append([x,y])

    return En

def invdictionary2(n): # a dictionary with inverses of permutations - so we need not calculate them every time!
    dict = {}
    for perm in itertools.permutations(range(1,n+1)):
        inv = [None]*n
        for k in range(n):
            inv[perm[k]-1] = k+1
        dict.update({perm:inv})
    return dict

#print(invdictionary(4))

def param_files(n):

    dict = invdictionary2(n-1)
    perms = [list(P) for P in itertools.permutations(range(1,n))]
    inv = [dict[P]+[n] for P in itertools.permutations(range(1,n))]
    enum = squenumerate(n-1)
    list_of_posets = [poset_binary(P[0]) for P in partial_orders(n-1)]

    file_number = 0

    for P in list_of_posets:

        file_number += 1

        params = open(f'non_discrete{n}_{file_number}.param' , 'w')

        print(f"language ESSENCE' 1.0 \n \nletting P be {P}\n", file = params)
        print(f"letting n be {n} \n", file = params)
        print(f"letting fac be {math.factorial(n-1)} \n", file = params)
        print(f"letting sq be {(n-1)*(n-1)} \n", file = params)
        print(f"letting enum be {enum} \n", file = params)
        print(f"letting perms be {perms} \n", file=params)
        print(f"letting invs be {inv}", file = params)

    return file_number

def construct_nondiscrete(n):
    num = param_files(n)
    all_sols = 0
    time1 = time.time()
    for k in range(2,num+1):
        print(f"Case {k} of {num}:")
        time3 = time.time()
        os.system(f'savilerow ./lalg_of_poset.eprime ./non_discrete{n}_{k}.param -run-solver -solver-options "-split" -all-solutions -solutions-to-stdout-one-line | grep --only-matching "\[\[.*\]\]" > L{n}_{k}')
        output = subprocess.check_output(f'cat ./non_discrete{n}_{k}.param.info | grep "SolverSolutionsFound" | grep -E --only-matching "[[:digit:]]*"', shell=True)
        new_sols = int(output)
        all_sols += new_sols
        time4 = time.time()
        print(f"We have found {new_sols} solutions in {time4-time3} seconds.")
    time2 = time.time()
    os.system('rm ./poset.size*')
    print(f"There are {all_sols} L-Algebras of size {n}. The search took {time2-time1} seconds.")

def enumerate_nondiscrete(n):
    num = param_files(n)
    all_sols = 0
    time1 = time.time()
    for k in range(2,num+1):

        # Skip the case where the poset is the diamond 
        if k == n-1:
            print("We have skipped the case where the poset is the diamond.")
            continue

        print(f"Case {k} of {num}:")
        time3 = time.time()
        os.system(f'savilerow ./lalg_of_poset.eprime ./non_discrete{n}_{k}.param -run-solver -solver-options "-split" -all-solutions -solutions-to-null| grep --only-matching "\[\[.*\]\]"')
        output = subprocess.check_output(f'cat ./non_discrete{n}_{k}.param.info | grep "SolverSolutionsFound" | grep -E --only-matching "[[:digit:]]*"', shell=True)
        new_sols = int(output)
        all_sols += new_sols
        time4 = time.time()
        print(f"We have found {new_sols} solutions in {time4-time3} seconds.")
    os.system('rm *.minion')
    time2 = time.time()
    print(f"There are {all_sols} L-Algebras of size {n}. The search took {time2-time1} seconds.")

def construct_nondiscrete(n):
    num = param_files(n)
    all_sols = 0
    time1 = time.time()
    for k in range(2,num+1):

        # Skip the case where the poset is the diamond 
        if k == n-1:
            print("We have skipped the case where the poset is the diamond.")
            continue

        print(f"Case {k} of {num}:")
        time3 = time.time()
        os.system(f'savilerow ./lalg_of_poset.eprime ./non_discrete{n}_{k}.param -run-solver -solver-options "-split" -all-solutions -solutions-to-stdout-one-line| grep --only-matching "\[\[.*\]\]" > non_discrete{n}_{k}.output')

        os.system(f'bzip2 non_discrete{n}_{k}.output')
        output = subprocess.check_output(f'cat ./non_discrete{n}_{k}.param.info | grep "SolverSolutionsFound" | grep -E --only-matching "[[:digit:]]*"', shell=True)
        new_sols = int(output)
        all_sols += new_sols
        time4 = time.time()
        print(f"We have found {new_sols} solutions in {time4-time3} seconds.")
    os.system('rm *.minion')
    time2 = time.time()
    print(f"There are {all_sols} L-Algebras of size {n}. The search took {time2-time1} seconds.")



#enumerate_nondiscrete(8)
construct_nondiscrete(6)
