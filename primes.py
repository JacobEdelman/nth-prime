import math
import bisect
import sys

memoized_pi = {}
memoized_phi = {}
prev = [2]
top = 2
def prime(n):

    log_n = math.log(n)
    loglog_n = math.log(log_n)
    if n> 7*10**5:
        min_p = n*int(log_n + loglog_n -1 ) -1 # cause <# cause <
        max_p = n*int(log_n + loglog_n + (math.log(math.log(n))-2)/log_n) # or loglog_n-2
    else:
        min_p = n*int(log_n) -1 # cause <# cause <
        max_p = n*int(log_n + loglog_n)
    sieve = primes(int(math.sqrt(max_p)))
    need = n - pi(min_p)
    if min_p == 2 and max_p == 3:
        return 3
    ret = []
    min_p = int(min_p)
    min_p += min_p%2 # make even
    max_p = int(max_p)
    #double counting some
    if need == 0:
        return min_p # should not be possible
#    seive = []
    for p_test in range(min_p+1,max_p+1, 2):
        if all(p_test%test != 0 for test in sieve):
            need -=1
            if need == 0:
                return p_test
def sub_pi(m):
    place = bisect.bisect(prev,m)
    if place != len(prev):
        return place
    if m in memoized_pi:
        return memoized_pi[m]
    if m == 1:
        return 0
    if m == 2:
        return 1
    y = math.ceil(m**(1.0/3)) # closest int above less than sqrt
    n = sub_pi(y)
    ret = phi(int(m),int(n)) +n -1 -P_2(m,n, y)
    memoized_pi[m] = ret
    return ret

def pi(m):
    primes(int(math.sqrt(int(m))))
    return sub_pi(int(m))

def upper_bound(n):
    return n*int(log_n + loglog_n)


def bth_prime(i):
    if i<=len(prev):
        return prev[i-1]
    v = 1
    while len(prev) < i:
        v *= 2
        primes(v)
    return prev[i-1]

def phi(m, b):
    #I made sure the stuff are integers
    # computed at start
    if (m,b) in memoized_phi:
        return memoized_phi[(m,b)]
    if b == 0:
        return m

    p = prev[b-1]
    # threadable
    ret = phi(m, b-1) - phi(m//p,b-1)
    memoized_phi[(m,b)] = ret
    return ret

def primes(max_p): #p<=max

    if max_p < 3:
        return [2]
    global prev
    global top
    if max_p <= top:
        return prev[:bisect.bisect(prev,max_p)]
    min_p = int(math.sqrt(max_p))
    if prev[-1] < min_p:
        primes(min_p) #gens primes
    else:
        min_p = top
    # min_p = 1
    # 3 - 1  not including 1 really... 3 -1 = 2, correct, +1 for each
    next_primes = [True]*(max_p-min_p) # starts at min_p+1
    # max_p = normal len ... min_p = where we are starting after
    to_add = []
    for i in prev:
        # 4 - 1 = 3
        j = i * i - min_p
        while j<1:
            j +=i
        x = len(next_primes)
        while j <= len(next_primes):
            next_primes[j-1] = False
            j += i
    for index, i in enumerate(next_primes):
        if i:
            to_add.append(index + min_p + 1)
    prev += to_add
    top = max_p
    return prev

# I should prevent overlap of int(math.sqrt(max_p)) and min_p
def primes_between(min_p, max_p): #min<p<=max
    x = primes(max_p)
    return x[bisect.bisect(x,min_p):]

def P_2(m,n, y):
    return sum(sub_pi(m/p) - sub_pi(p) +1 for p in primes_between(int(y),int(math.sqrt(m))))

def test(n):
    global memoized_pi
    global memoized_phi
    memoized_pi = {}
    memoized_phi = {}
    global times
    times = 0
    global prev
    prev = [2,3]
    a = pi(n)
    return times
if __name__ == '__main__':
    print prime(long(sys.argv[1]))
