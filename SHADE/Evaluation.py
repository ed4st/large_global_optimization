import numpy as np
from random import choices
import SHADE
from cec2013lsgo.cec2013 import Benchmark
import time
import argparse

'''
F1 elliptic
F2 rastrigin
F3 Ackley
F7 Schwefel
F12 Rosenbrock
¿F15 Schwefel?
'''

def Sphere(x):
    return np.dot(x,x)


def Compute(output_file,Fun,lower_limit,upper_limit,max_FE,NP=100,LP=100,D=1000):
    f=open(output_file,"a")
    start=time.time()
    shade=SHADE.SHADE(Fun,lower_limit,upper_limit,max_FE,NP,LP,D)
    opt=shade.solve()
    end=time.time()
    elapse_time=end-start
    #f.write(str(opt)+","+str(elapse_time)+","+str(D)+"\n")
    f.write("best="+str(opt)+"\n")
    f.write("time="+str(elapse_time)+"\n")
    f.write("dimension="+str(D)+"\n")
    f.close()

def main(args):
    bench=Benchmark()
    functions={"Sphere":{"Fun":Sphere,"lower":-100,"upper":100},
               "Elliptic":{"Fun":bench.get_function(1),"lower":bench.get_info(1)['lower'],"upper":bench.get_info(1)['upper']},
               "Rastrigin":{"Fun":bench.get_function(2),"lower":bench.get_info(2)['lower'],"upper":bench.get_info(2)['upper']},
               "Ackley":{"Fun":bench.get_function(3),"lower":bench.get_info(3)['lower'],"upper":bench.get_info(3)['upper']},
               "Rosenbrock":{"Fun":bench.get_function(7),"lower":bench.get_info(7)['lower'],"upper":bench.get_info(7)['upper']},
               "Schwefel":{"Fun":bench.get_function(15),"lower":bench.get_info(15)['lower'],"upper":bench.get_info(15)['upper']}}

    if args.LP:
        LP=args.LP
    else:
        LP=args.Pop_size
    Compute(args.output_file,
            functions[args.Fun]["Fun"],
            functions[args.Fun]["lower"],
            functions[args.Fun]["upper"],
            args.max_fun_evals,
            args.Pop_size,
            LP,
            args.Dimension)

if __name__ == '__main__':
    parser= argparse.ArgumentParser(description="Runs the SHADE algorithm")
    parser.add_argument("output_file",help="Name fo the file to save the output")
    parser.add_argument("Fun",help="Name of the function.",choices=["Sphere", "Elliptic", "Rastrigin", "Ackley", "Rosenbrock", "Schwefel"])
    parser.add_argument("max_fun_evals", help="Maximum number of evaluations",type=int)
    parser.add_argument("Pop_size", help="Size of the population",type=int)
    parser.add_argument("Dimension", help="Dimension of the problem",type=int)
    parser.add_argument("--LP",help="Size of the discrete memory for CR and F. Default is LP=Pop_size",type=int)
    main(parser.parse_args())