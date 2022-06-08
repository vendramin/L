import itertools
import math
import sys,os,time,subprocess
import copy

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

#print(invdictionary2(5))

def make_2sl(n):
    perms = [list(P) for P in itertools.permutations(range(1,n-1))]

    params = open(f'2sl_rel.param' , 'w')

    print(f"language ESSENCE' 1.0 \n\n", file = params)
    print(f"letting n be {n-2} \n", file = params)
    print(f"letting fac be {math.factorial(n-2)} \n", file = params)
    print(f"letting perms be {perms} \n", file=params)

    params.close()

def enumerate(n):
    make_2sl(n)

    os.system(f'savilerow ./2sl_relations.eprime ./2sl_rel.param -run-solver -all-solutions -solutions-to-stdout-one-line | grep --only-matching "\[\[.*\]\]" > 2sls_{n}')

    file = open(f'2sls_{n}', 'r')
    lines = file.readlines()

    enum = squenumerate(n-2)
    perms = [list(P) for P in itertools.permutations(range(1,n-1))]
    dict = invdictionary2(n-2)
    invs = [dict[tuple(P)]+[n-1,n] for P in dict]
    sq = (n-2)*(n-2)

    case_number = 0

    for l in lines:
        case_number += 1

        params = open(f'diamond{n}_{case_number}.param' , 'w')

        print(f"language ESSENCE' 1.0 \n letting R be {l} \n", file = params)
        print(f"letting n be {n} \n", file = params)
        print(f"letting fac be {math.factorial(n-2)} \n", file = params)
        print(f"letting perms be {perms} \n", file=params)
        print(f"letting invs be {invs} \n", file=params)
        print(f"letting enum be {enum} \n", file=params)
        print(f"letting sq be {sq} \n", file=params)

        params.close()

    os.system(f'rm ./2sls_{n}')

    all_sols = 0

    time3 = time.time()

    for k in range(1,case_number+1):
        print(f"Case {k} of {case_number}")
        time1 = time.time()
        os.system(f'savilerow ./diamond.eprime ./diamond{n}_{k}.param -run-solver -all-solutions -solutions-to-null')
        output = subprocess.check_output(f'cat ./diamond{n}_{k}.param.info | grep "SolverSolutionsFound" | grep -E --only-matching "[[:digit:]]*"', shell=True)
        new_sols = int(output)
        time2 = time.time()
        print(f"We have found {new_sols} solutions in {time2-time1} seconds.")
        all_sols += new_sols

    time4 = time.time()

    print(f"We have found {all_sols} diamond L-Algebras of size {n} in {time4-time3} seconds. Yay!")

enumerate(8)
