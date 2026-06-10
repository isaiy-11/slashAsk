import pickle


def save_chunks(chunks, file_path):

    with open(file_path, "wb") as file:
        pickle.dump(chunks, file)


def load_chunks(file_path):

    with open(file_path, "rb") as file:
        return pickle.load(file)