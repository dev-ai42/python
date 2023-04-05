def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)


def memoize(f):
    cache = {}
    def memo_f(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    #memo_f.cache = cache
    return memo_f

#fib2 = memoize(fib)
fib = memoize(fib)



#print(memoizedfib(35))
#print(memoizedfib(35))
#print(memoizedfib(34))

print(fib2(35))
print(fib2(35))
print(fib2(34))



