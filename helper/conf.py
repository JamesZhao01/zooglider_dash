from re import I
import sklearn
import pandas as pd
from sklearn.metrics import confusion_matrix
from collections import defaultdict
import numpy as np

def create_confusion_mat(df):
    true, pred = df["Ground Truth"], df["Prediction"]
    mat = confusion_matrix(true, pred)
    rowsum, colsum, diag = np.sum(mat, axis=1), np.sum(mat, axis=0), np.diag(mat)
    vert, horiz = np.nan_to_num(diag/rowsum), np.nan_to_num(diag/colsum)
    return mat, sorted(df["Ground Truth"].unique()), vert, horiz

def modify_mat(confu):
    relevant = np.sum(confu, axis=1)
    mat = confu / relevant.reshape((-1, 1))
    diag = np.diag(mat)
    mat = np.clip(-mat, -0.2, 1)
    np.fill_diagonal(mat, diag)
    return mat

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
