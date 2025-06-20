import pandas as pd
def save_to_csv(file_path, filtered_lines):
    if not file_path.endswith(".csv"):
        print(f"Warning: {file_path} does not end with .csv")
        exit(1)
    data_dict = {}
    for line in filtered_lines:
        if not line.startswith("####"):
            print(f"Warning: {line} does not start with ####")
            exit(1)
        line = line[4:]  # Remove the "####" prefix
        splited_lines = line.split(':')
        assert len(splited_lines) == 2, f"Error: {line} does not have exactly one colon"
        key = splited_lines[0].strip()
        value = splited_lines[1].strip()
        try:
            num = float(value)
            # Check if it's actually an integer value
            if num.is_integer():
                formatted_value = f"{int(num)}"
            else:
                formatted_value = f"{num:.2f}"
        except ValueError:
            formatted_value = value  # Keep as string if not a number
        data_dict[key] = [formatted_value]

    df = pd.DataFrame(data_dict)
    
    # for Figure 8 in the paper
    if "CSHeaps" in df.columns and "AllHeaps" in df.columns:
        df["CSHeaps"] = df["CSHeaps"].astype(int)
        df["AllHeaps"] = df["AllHeaps"].astype(int)
        df["CSHeapRatio"] = (df["CSHeaps"] / df["AllHeaps"]).apply(lambda x: f"{x:.2%}")
    
    # for Figure 11 in the paper
    if "Base" in df.columns and "Recursive" in df.columns:
        df["Base"] = df["Base"].astype(int)
        df["Recursive"] = df["Recursive"].astype(int)
        df["BaseRatio"] = (df["Base"] / df["Recursive"]).apply(lambda x: f"{x:.2%}")
        df['RecurRatio'] = (df["Recursive"] / df["Base"]).apply(lambda x: f"{x:.2%}")
    
    cols_to_front = ["T", "RM", "CE", "MFC", "PCS"]
    if "HeuristicTime" in df.columns:
        cols_to_front.extend(["HeuristicTime"])
    if "CSHeapRatio" in df.columns:
        cols_to_front.extend(["CSHeaps", "AllHeaps", "CSHeapRatio"])
    if "BaseRatio" in df.columns:
        cols_to_front.extend(["Base", "Recursive", "BaseRatio", "RecurRatio"])
    other_cols = [col for col in df.columns if col not in cols_to_front]
    df = df[cols_to_front + other_cols]
    
    df.to_csv(file_path, index=False)
