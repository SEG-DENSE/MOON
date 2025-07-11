import os
import subprocess
from util.benchmark import BENCHMARKS
from helper import save_to_csv
dir_name = "result-abletion"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
else:
    input(f"{dir_name} exists, press any key to confirm to override results in it.")


run = 0
for idx, app in enumerate(BENCHMARKS):
    for algo in ["MOONb"]:
        for sens in ["2o", "3o"]: # , 
            print(f"No.{run}: current app: {app}, index: {idx}/{len(BENCHMARKS)}, algo: {algo}, sens: {sens}")
            run += 1
            file_path = f"./{dir_name}/{app}_{algo}_{sens}.csv"

            command = f"python run.py {sens} {app} -print -cd -cda={algo}"
        
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )
                
            if result.returncode != 0:
                print(f"Error running command: {command}")
                print(result.stdout)
                continue
            filtered_lines = [line for line in result.stdout.splitlines() if line.startswith("####")]
            save_to_csv(file_path, filtered_lines)
