import os


def has_classification(exp_path):
    classification_csv = os.path.join(
        exp_path, "outputs", "classifications_for_all.csv")
    return None if not os.path.exists(classification_csv) else classification_csv
