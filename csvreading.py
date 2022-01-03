import os
import pandas as pd

csv = pd.read_csv("./assets/classifications_for_all.csv")
st =  "/d_sarafian/datasets/UVP5_processed_sep_2021/Acantharea/71078342_0.jpg"

for idx, (path, truth, pred) in csv.iterrows():
    spl = path.split("/")[-1]
    print(spl, truth, pred)
