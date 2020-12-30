import speech_recognition as sr
from pprint import pprint

def recognize(file):
    r = sr.Recognizer()
    test_speech = sr.AudioFile(file)
    with test_speech as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language='ko-KR', show_all=True)

    return result


if __name__ == '__main__':
    wav_file = 'sample_data/t2_0001.wav'
    result = recognize(wav_file)

    pprint(result)