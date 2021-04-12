import json


def load_json(data_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


def get_word():
    """Get next word in the interactive mode."""
    word = ""
    try:
        word = input("INPUT> ")
        if not issubclass(type(word), str):
            word = str(word, encoding="utf-8", errors="replace")
    except EOFError:
        pass
    if not word:
        pass
    return word