import os

def extract_results(data, line):
    terms = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC AUC Score"]
    # line = *** Testing, line + 1 = "Testing ...", line + 2 = "Computing ...", line + 3 starts the logs

    res = {}
    for i, x in enumerate(terms):
        if x not in data[line + i + 3]:
            print(x, line, data[line + i + 3])
            return None
        l = data[line + i + 3] # extracted line
        res[x] = float(data[line + i + 3][l.index(x) + len(x) + 2:])
    return res

def strip_time(l):
    return l[(l.index("INFO") + len("INFO: ")):]

def extract_training_logs(data, line, end):
    # line = ***Training***, line + 1 = "Training trial.."
    queries = ["Total time used: ", "Epoch ", "time used: ", "train loss: ", "val loss: "]
    line += 2
    logs = []
    while line < end:
        if data[line].startswith("Finished"):
            line += 1
            continue
        row = strip_time(data[line])
        if not row.startswith("Total time"):
            line += 1
            continue
        temp = row
        substrings = []
        for i in range(len(queries)):
            i1 = temp.index(queries[i])
            i2 = -1
            if i != len(queries) - 1:
                i2 = temp.index(queries[i + 1])
            substrings.append(temp[(i1 + len(queries[i])):i2].strip())
            temp = temp[i2:]
        logs.append(dict(zip(map(lambda x : x.strip(), queries), substrings)))
        line += 1
    return logs
def parse_log_file(path):
    if not os.path.exists(path):
        raise Exception(f"Parse log file: {path} not found")
    with open(path, "r") as f:
        lines = f.readlines()
        lines = list(map(lambda x : x.strip(), lines))
        # start by reading contains ************ Training ************
        query_tr = "************ Training ************"
        query_te = "************ Testing ************"
        line_tr, _ = next(((i,v) for i, v in enumerate(lines) if v.endswith(query_tr)), None)
        line_te, _ = next(((i,v) for i, v in enumerate(lines) if v.endswith(query_te)), None)
        if line_tr is None or line_te is None:
            return None
        train_logs = extract_training_logs(lines, line_tr, line_te)
        res = extract_results(lines, line_te)
        return train_logs, res
if __name__ == "__main__":
    parse_log_file("../train.log")