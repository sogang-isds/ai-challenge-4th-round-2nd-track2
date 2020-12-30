# 인공지능 그랜드 챌린지 4차 대회 2단계 트랙2 API

그랜드 챌린지 4차 대회 2단계에서 수행했던 모델을 API 버전으로 공개합니다. 리더보드에서 가장 높은 성적을 보였던 모델을 API 버전으로 제작하였습니다.



## Examples

파이썬 버전의 예제코드를 돌리려면 아래 명령을 입력합니다.

```bash
python example.py
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

