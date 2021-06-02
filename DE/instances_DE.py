import time
from DE import DifferentialEvolution
import numpy as np
from function import Benchmark
import csv
   
        
if __name__ == '__main__':
    
    with open('DE_results.csv', 'w', encoding = 'UTF8') as f:
        writer = csv.writer(f)
        
        bench = Benchmark()
        header = ['runtime', 'function_id', 'value' ,'time', 'dim']
        writer.writerow(header)
        
        for dimension in [10,30,50]:
            for runtime in range(5):
                for i in range(6):
                    start_time = time.time()
                    function = bench.get_function(i+1)
                    de = DifferentialEvolution(function = function,dim=dimension)
                    val_function = de.solve() #minimum value of remaining functions
                    writer.writerow([runtime+1, i+2, val_function, time.time() - start_time, dimension])
                    print(f"runtime number: {runtime}, dimension: {dimension}, function: {i+1}")
