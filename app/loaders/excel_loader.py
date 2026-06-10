import pandas as pd


def load_excel(file_path: str) -> str:
    """
    Reads Excel file
    and converts it to text.
    """

    df = pd.read_excel(file_path)

    return df.to_string(index=False)