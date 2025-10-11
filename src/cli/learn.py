import argparse
from quacq.core import *
from quacq.acquisition import QuAcq, Solve
from utils.logger import setup_logger, writelog
from benchmarks import zebra, jigsaw, rflap, murder
import random
import json
import time
import os




def main(benchmark, output,logger=None):

    writelog(logger,f"start learning the benchmark {benchmark} using quacq algorithm")    
    
    # 1. Load selected benchmark
    benchmark_map = {
        "zebra": zebra,
        "jigsaw": jigsaw,
        "murder": murder,
        "rflap": rflap
    }
    
    model = benchmark_map[benchmark].Model()

    # 2. Create target network
    t = Target_Network(model.constraints)

    L = QuAcq(B=model.bais, variables=model.variables, target_network=t,logger=logger)
    

    # convergence check
    sol=Solve(L,model.variables)
    if len(sol) == 0: writelog(logger,'no solution found',level="error")
    # 3. Output results
    
    output_data={
        "method":"QuAcq",
        "benchmark":benchmark,
        "query":t.ask_counter,
    }
    
    # 4. Save output
    id = f"{int(time.time()*1000)}_{random.randint(1000,9999)}"

    os.makedirs(output, exist_ok=True)
    with open(f"{output}/{id}.json", "w") as f:
        json.dump(output_data,f)
    


if __name__=="__main__":

    logger = setup_logger(to_console=True)
    parser = argparse.ArgumentParser(description="Constraint Acquisition with GNN")

    parser.add_argument("--benchmark", type=str, choices=["zebra" , "jigsaw","murder","rflap"], required=True,
                        help="Select the benchmark problem to run.")
             
    parser.add_argument("--output", type=str, default="results",
                        help="Path to the output results file.")
   
    args = parser.parse_args()
    
    main(**args.__dict__ | {'logger':logger})