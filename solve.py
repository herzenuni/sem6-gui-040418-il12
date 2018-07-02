import numpy

def solve(a):
    b = []
    for i in range(len(a)):
        b.append(a[i].pop())
    print(numpy.linalg.solve(a,b))
    return numpy.linalg.solve(a,b)
