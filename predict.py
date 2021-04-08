import os
from os import environ
from psutil import cpu_count

# Constants from the performance optimization available in onnxruntime
# It needs to be done before importing onnxruntime
environ["OMP_NUM_THREADS"] = str(cpu_count(logical=True))
environ["OMP_WAIT_POLICY"] = 'ACTIVE'

from onnxruntime import InferenceSession, SessionOptions, get_all_providers
from transformers import AutoTokenizer


def create_model_for_provider(model_path: str, provider: str) -> InferenceSession:
    assert provider in get_all_providers(), f"provider {provider} not found, {get_all_providers()}"

    # Few properties than might have an impact on performances (provided by MS)
    options = SessionOptions()
    options.intra_op_num_threads = 1

    # Load the model as a graph and prepare the CPU backend
    return InferenceSession(model_path, options, providers=[provider])


curdir = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(curdir, 'models/test')
onnx_path = os.path.join(curdir, 'models/model_fp16.onnx')

tokenizer = AutoTokenizer.from_pretrained('beomi/kcbert-base')

onnx_model = create_model_for_provider(onnx_path, "CPUExecutionProvider")

# Inputs are provided through numpy array
model_inputs = tokenizer.encode_plus("Hello", return_tensors="pt")
inputs_onnx = {k: v.cpu().detach().numpy() for k, v in model_inputs.items()}

# Run the model (None = get all the outputs)
logits = onnx_model.run(None, inputs_onnx)

import numpy as np

print(logits[0])
print(np.argmax(logits[0], axis=1))
