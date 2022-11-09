## 요구조건
- docker >= 1.12.0
- docker-compose >= 1.6.0

## 실행

```
docker-compose up
```

## 오류해결


- "python/r" 을 찾을 수 없다는 오류
  - CRLF, LF 문제니 git 설정을 아래와 같이 바꿀 것
  - 그리고 모든 파일의 포맷을 LF 포맷으로 바꿀 것
```
git config --global core.eol lf
git config --global core.autocrlf input
```