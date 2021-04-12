import json
import speech_recognition as sr

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


def recognize(file):
    r = sr.Recognizer()
    test_speech = sr.AudioFile(file)
    with test_speech as source:
        # r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    result = r.recognize_google(audio, language='ko-KR', show_all=True)

    return result