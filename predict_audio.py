import os
from os import environ
from psutil import cpu_count
import numpy as np
import time

# Constants from the performance optimization available in onnxruntime
# It needs to be done before importing onnxruntime
environ["OMP_NUM_THREADS"] = str(cpu_count(logical=True))
environ["OMP_WAIT_POLICY"] = 'ACTIVE'

from onnxruntime import InferenceSession, SessionOptions, get_all_providers
from transformers import AutoTokenizer

from utils import load_json, get_word, recognize
from audio_splitter_example import split_audio

def create_model_for_provider(model_path: str, provider: str) -> InferenceSession:
    assert provider in get_all_providers(), f"provider {provider} not found, {get_all_providers()}"

    # Few properties than might have an impact on performances (provided by MS)
    options = SessionOptions()
    options.intra_op_num_threads = 1

    # Load the model as a graph and prepare the CPU backend
    return InferenceSession(model_path, options, providers=[provider])


label_dict = load_json(os.path.join('sample_data/label_dict.json'))
label_list = [x for x, y in label_dict.items()]


curdir = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(curdir, 'models/test')
onnx_path = os.path.join(curdir, 'models/model_fp16.onnx')

tokenizer = AutoTokenizer.from_pretrained('beomi/kcbert-base')

onnx_model = create_model_for_provider(onnx_path, "CPUExecutionProvider")


def predict(input_file, tmp_path='./tmp'):
    positions = split_audio(input_file, dest_path=tmp_path)

    files = os.listdir(tmp_path)
    files = sorted(files)

    wav_files = []

    for file in files:
        wav_files.append(os.path.join(tmp_path, file))

    #
    # 음성인식 처리
    #
    print('\nSpeech recognizing...')
    trans = []
    for wav_file in wav_files:
        if not wav_file.split('/')[-1].startswith('chunk'):
            continue

        result = recognize(wav_file)
        transcript = result['alternative'][0]['transcript'] if len(result) > 0 else ''

        trans.append(transcript)

        try:
            print(f'recognized :{wav_file}, {transcript}')
        except UnicodeEncodeError:
            print(f'recognition failed : {wav_file}')

        time.sleep(0.05)

    return trans


while True:
    try:
        print('\n파일 경로를 입력하세요.')
        input_file = get_word()
        text_list = predict(input_file)

        print('\nPredicting...')
        text = ' '.join(text_list)

        # Inputs are provided through numpy array
        model_inputs = tokenizer.encode_plus(text)
        inputs_onnx = {k: np.array(v).reshape(1, -1) for k, v in model_inputs.items()}

        # Run the model (None = get all the outputs)
        logits = onnx_model.run(None, inputs_onnx)

        pred_idx = int(np.argmax(logits[0], axis=1))
        label = label_list[pred_idx]

        print(f'{label}, {label_dict[label]}')

    except Exception as e:
        import traceback

        print(e)
        print(traceback.print_exc())
