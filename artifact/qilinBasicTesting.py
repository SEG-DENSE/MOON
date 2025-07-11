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


def runCommand(command, output_file):
    print(command)
    subprocess.run(command, shell=True, stdout=output_file, stderr=output_file)
    pass
run = 0
selected_benchmarks = ["antlr", "biojava", "fop", "h2"]
for idx, app in enumerate(selected_benchmarks):
    for sens in [ "2o"]: # 
        for algo in ["MOON"]: # 
            print(f"current app: {app}, index: {idx}/{len(selected_benchmarks)}, algo: {algo}, sens: {sens}")
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

            result = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )
            filtered_lines = [line for line in result.stdout.splitlines() if line.startswith("####")]
            save_to_csv(file_path, filtered_lines)
