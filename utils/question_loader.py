import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATHS = {
    "DSA": os.path.join(BASE_DIR, "data", "dsa_questions.csv"),
    "DBMS": os.path.join(BASE_DIR, "data", "dbms_questions.csv"),
    "OOP": os.path.join(BASE_DIR, "data", "oop_questions.csv"),
    "OS": os.path.join(BASE_DIR, "data", "os_questions.csv"),
    "CN": os.path.join(BASE_DIR, "data", "cn_questions.csv"),
    "ML": os.path.join(BASE_DIR, "data", "ml_questions.csv")
}


def load_questions(subject):
    file_path = DATA_PATHS.get(subject)

    if file_path and os.path.exists(file_path):
        return pd.read_csv(file_path)

    return pd.DataFrame()