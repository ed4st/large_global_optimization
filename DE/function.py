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
        '''
        Return the value of the following function:
        f(x) = x1^2 + x2^2 + x3^2 + ... xn^2

        Parameters:
        ---------------------------
        x : np.array
        '''
        return np.dot(x,x)
    
    def __elliptic(self, x):
        D=x.shape[0]
        sq_x=np.square(x)
        t=np.array([np.power(10,6*(i-1)/(D-1)) for i in range(1,D+1)])
        return np.dot(t,sq_x)

    def __rastringin(self, x):
        D=x.shape[0]
        sq_x=np.square(x)
        cosx=np.cos(2*np.pi*x)
        return (np.sum(sq_x)+np.sum(cosx)+D*10)
    def __ackley(self, x):
        D = len(x)
        return -20*np.exp(-.2*np.sqrt((1/D)*np.dot(x,x)) - np.exp((1/D)*sum(np.cos(2*np.pi*x)))) + 20 +np.e
    def __schwefel(self, x):
        csum=np.sum(x)
        sq_csum=np.square(csum)
        return np.sum(sq_csum)
    def __rosenbrock(self, x):
        D = len(x)
        return sum([100*(x[i]**2- x[i+1])**2 + (x[i] - 1)**2 for i in range(D-1)] )
