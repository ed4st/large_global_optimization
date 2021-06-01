import numpy as np


class Benchmark():
    def __init__(self):
        pass
    
    def get_function(self, index = 1):
        if index == 2:
            return self.__elliptic
        if index == 3:
            return self.__rastringin
        if index == 4:
            return self.__ackley
        if index == 5:
            return self.__schwefel
        if index == 6:
            return self.__rosenbrock
        else:
            return self.__sphere
        
    def __sphere(self, x):
        return np.dot(x,x)
    
    def __elliptic(self, x):
        pass
    def __rastringin(self, x):
        pass
    def __ackley(self, x):
        D = len(x)
        return -20*np.exp(-.2*np.sqrt((1/D)*np.dot(x,x)) - np.exp((1/D)*sum(np.cos(2*np.pi*x)))) + 20 +np.e
    def __schwefel(self, x):
        pass
    def __rosenbrock(self, x):
        pass

bench = Benchmark()
function = bench.get_function(1)
print(function(np.array([1,2])))
