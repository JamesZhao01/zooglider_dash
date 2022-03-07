from re import I
import sklearn
import pandas as pd
from sklearn.metrics import confusion_matrix
from collections import defaultdict


def create_confusion_mat(df):
    true, pred = df["Ground Truth"], df["Prediction"]
    return confusion_matrix(true, pred), sorted(df["Ground Truth"].unique())


def make_dicts(df):
    index = []
    correct = defaultdict(list)
    ground_miss = defaultdict(lambda: defaultdict(list))
    pred_miss = defaultdict(lambda: defaultdict(list))
    for i, (src, ground, pred) in df.iterrows():
        path = "/".join(src.split("/")[-2:])
        index.append(path)
        if ground == pred:
            correct[ground].append(i)
        else:
            ground_miss[ground][pred].append(i)
            pred_miss[pred][ground].append(i)
    return correct, ground_miss, pred_miss, index
