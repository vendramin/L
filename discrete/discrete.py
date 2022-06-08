import os, subprocess
import math, itertools
from time import time as gettime

def invdictionary(n): # a dictionary with inverses of permutations - so we need not calculate them every time!
    dict = {}
    for perm in itertools.permutations(range(1,n+1)):
        inv = [None]*n
        for k in range(n):
            inv[perm[k]-1] = k+1
        dict.update({perm:inv})
    return dict

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

def print_perms(n):

    dic = invdictionary(n)

    perms = [list(P) for P in dic.keys()]
#    inv = [dic[tuple(P)] for P in perms]

    sourceFile = open(f'perms{n}.param', 'w')

    print("language ESSENCE' 1.0 \nletting perms be ", end='', file = sourceFile)

    print(perms, file = sourceFile)

#    print("letting invs be ", end='')

#    print(inv)

    print("letting n be ", end='', file = sourceFile)

    print(n, file = sourceFile)

    print("letting fac be ", end='', file = sourceFile)

    print(math.factorial(n), file = sourceFile)

    sourceFile.close()

def construct_discrete(n):

    print_perms(n-1)

    os.system(f'savilerow ./disc_app_semilattice.eprime ./perms{n-1}.param -run-solver -all-solutions -solutions-to-stdout-one-line > semilattice_{n-1}')

    os.system(f'cat ./semilattice_{n-1} | grep --only-matching "\[\[\[\[.*\]\]\]\]" > app_semilattices{n-1}')

    os.system(f'rm ./semilattice_{n-1}')
    os.system(f'rm ./perms{n-1}*')

    file = open(f'app_semilattices{n-1}', 'r')
    lines = file.readlines()

    line_number = 0

    for line in lines:

        line_number += 1

        params = open(f'app_semi_{n-1}.{line_number}.param' , 'w')

        print(f"language ESSENCE' 1.0 \n \nletting M be {line}", file = params)
        print(f"letting n be {n} \n", file = params)
        print(f"letting fac be {math.factorial(n-1)} \n", file = params)
        print(f"letting sq be {(n-1)*(n-1)} \n", file = params)

        enum = squenumerate(n-1)

        print(f"letting enum be {enum} \n", file = params)

        perms = [list(P) for P in itertools.permutations(range(1,n))]

        print(f"letting perms be {perms} \n", file = params)

        dic = invdictionary(n-1)
        perms = [list(P) for P in perms]
        inv = [dic[tuple(P)] + [n] for P in perms]

        print(f"letting invs be {inv}", file = params)
        params.close()

    os.system(f'rm ./app_semilattices{n-1}')

    all_sols = 0

    time3 = gettime()

    for k in range(1,line_number+1):
        time1 = gettime()
        print(f"Case {k} of {line_number}")
        os.system(f'savilerow ./discrete.eprime ./app_semi_{n-1}.{k}.param -run-solver -all-solutions -solutions-to-stdout-one-line | grep --only-matching "\[\[.*\]\]" > discrete{n}_{k}')
        output = subprocess.check_output(f'cat ./app_semi_{n-1}.{k}.param.info | grep "SolverSolutionsFound" | grep -E --only-matching "[[:digit:]]*"', shell=True)

        new_sols = int(output)

        time2 = gettime()
        time = time2-time1
        all_sols += new_sols
        print(f"We have found {new_sols} solutions in {time}.")

    time4 = gettime()

    os.system(f'rm ./app_semi_{n-1}*')

    print(f"There are {all_sols} discrete L-Algebras of size {n}. The search took {time4-time3}.")

def enumerate_discrete(n):

    print_perms(n-1)

    os.system(f'savilerow ./disc_app_semilattice.eprime ./perms{n-1}.param -run-solver -all-solutions -solutions-to-stdout-one-line > semilattice_{n-1}')

    os.system(f'cat ./semilattice_{n-1} | grep --only-matching "\[\[\[\[.*\]\]\]\]" > app_semilattices{n-1}')

    os.system(f'rm ./semilattice_{n-1}')
    os.system(f'rm ./perms{n-1}*')

    file = open(f'app_semilattices{n-1}', 'r')
    lines = file.readlines()

    line_number = 0

    for line in lines:

        line_number += 1

        params = open(f'app_semi_{n-1}.{line_number}.param' , 'w')

        print(f"language ESSENCE' 1.0 \n \nletting M be {line}", file = params)
        print(f"letting n be {n} \n", file = params)
        print(f"letting fac be {math.factorial(n-1)} \n", file = params)
        print(f"letting sq be {(n-1)*(n-1)} \n", file = params)

        enum = squenumerate(n-1)

        print(f"letting enum be {enum} \n", file = params)

        perms = [list(P) for P in itertools.permutations(range(1,n))]

        print(f"letting perms be {perms} \n", file = params)

        dic = invdictionary(n-1)
        perms = [list(P) for P in perms]
        inv = [dic[tuple(P)] + [n] for P in perms]

        print(f"letting invs be {inv}", file = params)
        params.close()

    os.system(f'rm ./app_semilattices{n-1}')

    all_sols = 0

    time3 = gettime()

    for k in range(1,line_number+1):
        time1 = gettime()
        print(f"Case {k} of {line_number}")
        os.system(f'savilerow ./discrete.eprime ./app_semi_{n-1}.{k}.param -run-solver -all-solutions -solutions-to-null')
        output = subprocess.check_output(f'cat ./app_semi_{n-1}.{k}.param.info | grep "SolverSolutionsFound" | grep -E --only-matching "[[:digit:]]*"', shell=True)

        new_sols = int(output)

        time2 = gettime()
        time = time2-time1
        all_sols += new_sols
        print(f"We have found {new_sols} solutions in {time}.")

    time4 = gettime()

    os.system(f'rm ./app_semi_{n-1}*')

    print(f"There are {all_sols} discrete L-Algebras of size {n}. The search took {time4-time3}.")

enumerate_discrete(7)
