import os
import subprocess
from util.benchmark import BENCHMARKS
from moonConfig import unscalable
from helper import save_to_csv
dir_name = "result"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
else:
    input(f"{dir_name} exists, press any key to confirm to override results in it.")


def runCommand(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stdout)
    return result
run = 0
for idx, app in enumerate(BENCHMARKS):
    for sens in ["ci", "csc"]:
        print(f"current app: {app}, index: {idx}/{len(BENCHMARKS)}, sens: {sens}")
        command = f"python run.py {sens} {app} -print"
        file_path = f"./{dir_name}/{app}_{sens}.csv"

        result = runCommand(command)
        if result.returncode != 0:
            continue
        filtered_lines = [
            line for line in result.stdout.splitlines() if line.startswith("####")
        ]
        save_to_csv(file_path, filtered_lines)
    for sens in [ "2o", "3o"]: # 
        for algo in ["PLAIN", "MOON", "ZIPPER", "CONCH",  "DEBLOATERX"]: # 
            print(f"current app: {app}, index: {idx}/{len(BENCHMARKS)}, algo: {algo}, sens: {sens}")
            if (app, algo, sens, None) in unscalable:
                continue
            run += 1
            file_path = f"./{dir_name}/{app}_{algo}_{sens}.csv"

            command = ""
            if algo == "PLAIN":
                command = f"python run.py {sens} {app} -print"
            elif algo == "ZIPPER":
                command = f"python run.py Z-{sens} {app} -print"
            else:
                command = f"python run.py {sens} {app} -print -cd -cda={algo}"

            result = runCommand(command)
            if result.returncode != 0:
                continue
            
            filtered_lines = [line for line in result.stdout.splitlines() if line.startswith("####")]
            save_to_csv(file_path, filtered_lines)
