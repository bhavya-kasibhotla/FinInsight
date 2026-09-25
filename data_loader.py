import pandas as pd


def load_financial_data():
    file_path = "data/Financial Statements.csv"

    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    return df