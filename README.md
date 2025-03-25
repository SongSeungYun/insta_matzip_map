인스타그램 인플루언서 게시물 기반 맛집 지도

소개:
이 프로젝트는 인스타그램 인플루언서의 게시물을 기반으로 맛집 정보를 수집하고, 이를 지도에 표시하는 웹 애플리케이션입니다. 사용자는 밥집, 카페, 술집 카테고리별로 원하는 맛집 정보를 지도에서 확인하고, 관련된 소셜 미디어 링크와 지도 서비스를 통해 추가 정보를 얻을 수 있습니다.

주요 기능

인스타그램 크롤링: 인플루언서 계정의 게시물을 자동으로 크롤링하여 맛집 정보를 수집합니다.

AI 분석: Perplexity AI API를 활용해 게시물 텍스트에서 식당 정보를 추출합니다.

지도 표시: 카카오맵 API를 사용하여 맛집 위치를 지도에 시각적으로 표시합니다.

카테고리 필터링: 밥집, 카페, 술집 카테고리를 선택하여 마커를 필터링할 수 있습니다.

인포윈도우 제공: 각 맛집에 대한 상세 정보(이름, 주소, 메인 메뉴)와 관련된 링크(인스타 릴스, 구글 지도, 네이버 지도, 카카오맵)를 제공합니다.


설치 및 실행 방법

1. 프로젝트 클론
```
git clone https://github.com/SongSeungYun/insta_matzip_map
cd insta_matzip_map
```

2. Python 의존성 설치
requirements.txt 파일을 사용해 필요한 Python 패키지를 설치
```
cd get_data
pip install -r requirements.txt
```
3. Node.js 의존성 설치
Node.js 환경에서 필요한 패키지를 설치
```
cd ../back
npm install
```
4. 환경 변수 설정
data/secret.json 파일을 생성하고 아래 내용을 입력하세요:

```json
{
    "MAP_API_KEY": "카카오 맵 API 키",
    "Insta_ID": "인스타그램 아이디",
    "Insta_PW": "인스타그램 비밀번호",
    "AI_API_KEY": "Perplexity AI API 키"
}
```
5.원하는 인스타그램 인플루언서 추가

get_data/crawling.py로 이동해서 원하는 인스타그램 계정의 아이디를 적어주세요.
ex) account_id=["example1", "example2"]

추가로 기존 데이터를 없애고 싶으시면 data 폴더의 json파일들을 다음과 같이 수정해주세요.
```json
//post_count.json
{
    "dummy": 0,
    "hotdor_s": 166
}
```


6. 서버 실행
Python 크롤링 및 데이터 분석 실행:

cd ../get_data
python main.py

크롤링이 완료된 후 Node.js 서버 실행:

cd back
node app.js

7. 웹 애플리케이션 접속
브라우저에서 http://localhost:3000으로 접속하여 애플리케이션을 확인합니다.

사용법
1. 지도 인터페이스 탐색
카테고리 선택: 화면 상단의 메뉴(밥집, 카페, 술집)를 클릭하여 원하는 카테고리의 마커를 표시하거나 숨길 수 있습니다.

마커 클릭: 마커를 클릭하면 해당 맛집의 상세 정보(이름, 주소, 메인 메뉴)와 관련된 링크(인스타 릴스, 구글 지도, 네이버 지도, 카카오맵)가 표시됩니다.

2. 데이터 업데이트 (크롤링)
새로운 데이터를 가져오려면 Python 스크립트를 다시 실행하세요:

bash
python main.py
이 명령은 인스타그램에서 최신 게시물을 크롤링하고 AI를 통해 분석한 결과를 업데이트합니다.

파일 구조
text
INSTA_MATZIP_CRAWLING/
├── back/                     # Node.js 백엔드 코드
│   ├── public/               # 프론트엔드 정적 파일 (HTML, CSS, JS)
│   │   ├── css/              # 스타일 파일 (CSS)
│   │   ├── image/            # 마커 이미지 및 기타 이미지 파일
│   │   ├── javascript/       # 클라이언트 측 JavaScript 파일 (map.js)
│   │   └── views/            # EJS 템플릿 파일 (index.ejs)
│   ├── app.js                # Express 서버 설정 파일
│   └── package.json          # Node.js 패키지 설정 파일
├── data/                     # 데이터 저장 폴더
│   ├── secret.json           # API 키 및 환경 변수 설정 파일 (사용자 생성 필요)
│   ├── post_count.json       # 크롤링한 게시물 개수 기록 파일
│   └── restaurants_infos.json# 식당 정보 저장 파일
├── get_data/                 # 데이터 처리 모듈(Python)
│   ├── crawling.py           # 인스타그램 크롤링 코드
│   └── data_analyzing.py     # AI 데이터 분석 코드
├── main.py                   # Python 메인 실행 파일 (크롤링 및 데이터 분석)
├── requirements.txt          # Python 의존성 목록 파일
├── .gitignore                # Git에 포함되지 않을 파일 목록 설정 (.json 등 민감한 정보 제외)
└── README.md                 # 프로젝트 설명 문서 (현재 작성 중)
기술 스택
프론트엔드:
HTML/CSS/JavaScript: 사용자 인터페이스 구성.

카카오맵 API: 지도 서비스 제공.

백엔드:
Node.js + Express: 웹 서버 구축.

EJS: 템플릿 엔진을 사용한 동적 페이지 렌더링.

데이터 처리:
Python + Selenium: 인스타그램 크롤링.

Perplexity AI API: 텍스트 분석 및 식당 정보 추출.

geopy: 주소를 위도와 경도로 변환.
