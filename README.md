# 인공지능 그랜드 챌린지 4차 대회 2단계 트랙2

그랜드 챌린지 4차 대회 2단계에서 수행했던 모델을 공개합니다. 리더보드에서 가장 높은 성적을 보였던 모델을 API 버전으로 제작하였습니다.

## Requirements

* Python >= 3.6

### Git LFS

모델파일과 샘플데이터를 받기 위해서는 Git LFS가 필요합니다. 없을 경우 아래 링크를 이용해 설치합니다.

* [Git LFS Installation](https://github.com/git-lfs/git-lfs/wiki/Installation)

## Installation

* 아래 명령을 이용해 소스코드를 받습니다.

    ```
    https://github.com/sogang-isds/ai-challenge-4th-round-2nd-track2.git
    ```

* Git LFS가 자동으로 되지 않을 경우 아래 명령을 이용해 LFS 파일들을 내려받습니다.

    ```bash
    cd ai-challenge-4th-round-2nd-track2
    git lfs pull
    ```

* Python 가상환경을 설치합니다.

    ```bash
    cd ai-challenge-4th-round-2nd-track2
    virtualenv -p python3 myenv
    source myenv/bin/activate
    ```

* Python 패키지를 설치합니다.

    ```bash
    pip install -r requirements.txt
    ```

## Examples

분석하고자 하는 음성파일을 API를 통해 보내면 분석 후 클래스 코드를 리턴합니다. 예제 음성대화 파일은 `sample_data` 디렉토리에 있습니다.

**api_example.py**

```python
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
```

파이썬 버전의 예제코드를 돌리려면 아래 명령을 입력합니다.

```bash
python api_example.py
```

실행 결과로는 아래와 같이 JSON 형태로 받아보실 수 있습니다.

```
{
  "code": "E000", 
  "data": {
    "annotations": [
      {
        "class code": "020121", 
        "file_name": "t2_0001.wav"
      }
    ]
  }, 
  "msg": "Success"
}
```

## 응답 데이터

### code

- E000 : 성공

### class code

협박은 아래와 같이 5가지의 클래스로 분류됩니다.

- 000001 : 일반대화
- 020121 : 협박
- 02051 : 갈취 또는 공갈
- 020811 : 직장 내 괴롭힘
- 020819 : 기타 괴롭힘

## Copyright

본 프로젝트는 공개소프트웨어를 이용하여 개발하였으나, 데이터 처리 방법 및 모델 구현 등에 대한 저작권은 [서강대학교 지능형 음성대화 인터페이스 연구실](https://isds.sogang.ac.kr/)에 있습니다.

