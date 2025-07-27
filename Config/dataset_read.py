import pandas as pd


def read_dataframe(path):
    df = pd.DataFrame(pd.read_csv(path))
    return df