def load_txt(file_path: str) -> str:
    """
    Reads text from a TXT file
    """

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text