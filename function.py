import numpy as np


class Benchmark():
    def __init__(self):
        pass
    
    def get_function(self, index = 1):
        if index == 2:
            return self.__sphere
        if index == 3:
            return self.__sphere
        if index == 4:
            return self.__sphere
        if index == 5:
            return self.__sphere
        if index == 6:
            return self.__sphere
        else:
            return self.__sphere
        
    def __sphere(self, x):
        return np.dot(x,x)
    
    def __elliptic(self, x):
        pass
    def __rastringin(self, x):
        pass
    def __ackley(self, x):
        pass
    def __schwefel(self, x):
        pass
    def __rosenbrock(self, x):
        pass
    