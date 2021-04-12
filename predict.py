import os
from os import environ
from psutil import cpu_count
import numpy as np

# Constants from the performance optimization available in onnxruntime
# It needs to be done before importing onnxruntime
environ["OMP_NUM_THREADS"] = str(cpu_count(logical=True))
environ["OMP_WAIT_POLICY"] = 'ACTIVE'

from onnxruntime import InferenceSession, SessionOptions, get_all_providers
from transformers import AutoTokenizer

from utils import load_json, get_word


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

while True:
    try:
        text = get_word()

        # Inputs are provided through numpy array
        model_inputs = tokenizer.encode_plus(text, return_tensors="pt")
        inputs_onnx = {k: v.cpu().detach().numpy() for k, v in model_inputs.items()}

        # Run the model (None = get all the outputs)
        logits = onnx_model.run(None, inputs_onnx)

        pred_idx = int(np.argmax(logits[0], axis=1))
        label = label_list[pred_idx]

        print(f'{label}, {label_dict[label]}')

    except Exception as e:
        import traceback

        print(e)
        print(traceback.print_exc())
