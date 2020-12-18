import requests

url = 'http://163.239.28.23:5001/api/get_threat_result'

wav_file = 'sample_data/t2_0001.wav'
file_data = {'file': ('t2_0001.wav', open(wav_file, 'rb'), 'audio/wav')}
resp = requests.post(url, files=file_data)

if resp.status_code == requests.codes.ok:
    response_body = resp.content.decode('utf-8')
    print(response_body)
else:
    print('Error :', resp.status_code)