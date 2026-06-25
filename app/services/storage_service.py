import pickle


def save_chunks(chunks, file_path):

    with open(file_path, "wb") as file:
        pickle.dump(chunks, file)


def load_chunks(file_path):

    with open(file_path, "rb") as file:
        return pickle.load(file)


def append_chunks(new_chunks, file_path):

    try:
        with open(file_path, "rb") as file:
            existing_chunks = pickle.load(file)

    except:
        existing_chunks = []

    existing_chunks.extend(new_chunks)

    with open(file_path, "wb") as file:
        pickle.dump(existing_chunks, file)