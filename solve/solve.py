import numpy

def solve(a):
    b = []
    print(len(a))
    for i in range(len(a)):
        b.append(a[i].pop())
    return numpy.linalg.solve(a,b)
