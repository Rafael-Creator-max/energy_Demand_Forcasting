import pandas as pd 
import glob

files = glob.glob("../data/raw/*csv")

dfs =[]

for file in files:

    #Check the columns of the files

    with open(file, "r", encoding="utf-8") as f:
        first_line = f.readline()

    print(file)
    print(repr(first_line))

    #Detect seperator 
    with open(file, "r", encoding="utf-8") as f:
        first_line = f.readline()

    if ";" in first_line:
        sep = ";"
    else:
        sep = "\t"
    df = pd.read_csv(file, sep=sep)

    #Check if the files match with each other
    print(file)
    print(df.shape)
    print(df.columns)

    dfs.append(df)


combined_df = pd.concat(dfs)

combined_df.to_csv(
    "../data/processed/all_load_values.csv",
    index=False
)

print("Combined dataset saved.")


#Test 1
print(combined_df.shape)

