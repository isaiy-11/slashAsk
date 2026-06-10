import pandas as pd


def load_csv(file_path: str) -> str:
    """
    Reads data from a CSV file
    and converts it to text.
    """

    df = pd.read_csv(file_path)

    return df.to_string(index=False)
