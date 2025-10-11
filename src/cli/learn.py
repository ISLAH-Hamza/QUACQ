import argparse
from QUACQ.core import *
from QUACQ.acquisition import QuAcq
from benchmarks import zebra, jigsaw, rflap, murder
from QUACQ.utils import logger
import random
import json
import time
import os




def main():

    # 1. Argument parser
    parser = argparse.ArgumentParser(description="Constraint Acquisition with GNN")

    parser.add_argument("--benchmark", type=str, choices=["zebra" , "jigsaw","murder","rflap"], required=True,
                        help="Select the benchmark problem to run.")
             
    parser.add_argument("--output", type=str, default="results",
                        help="Path to the output results file.")
   

    args = parser.parse_args()


    log=logger.setup_logger()
    
    # 2. Load selected benchmark
    benchmark_map = {
        "zebra": zebra,
        "jigsaw": jigsaw,
        "murder": murder,
        "rflap": rflap
    }
    
    model = benchmark_map[args.benchmark].Model()

    # 3. Create target network
    t = Target_Network(model.constraints)

    L = QuAcq(B=model.bais, variables=model.variables, target_network=t,logger=log)
    
    # 5. Output results
    
    output={
        "method":"QuAcq",
        "benchmark":args.benchmark,
        "query":t.ask_counter,
    }
    
    # 6. Save output
    id = f"{int(time.time()*1000)}_{random.randint(1000,9999)}"

    os.makedirs(args.output, exist_ok=True)
    with open(f"{args.output}/{id}.json", "w") as f:
        json.dump(output,f)
    


if __name__=="__main__":
    main()