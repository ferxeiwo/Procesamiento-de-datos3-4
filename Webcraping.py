import pandas as pd


data = "./resultado.csv"

df = pd.read_csv(data, nrows=10)

if df.shape[0] > 0:
    print("datos extraidos")
else:
    print("no se extrajeron datos")

print(df)