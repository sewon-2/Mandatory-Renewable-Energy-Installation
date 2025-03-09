# 🚀 신재생에너지 의무공급비율 법규 검토 모델

## 📌 프로젝트 소개
**"신재생에너지 의무공급비율"** 법규 검토 시, 건축물의 신재생에너지 공급 비율을 자동으로 계산하는 서비스입니다.  
사용자가 입력한 정보를 기반으로 **Google Sheets API**를 활용하여 클라우드에 업로드 된 엑셀 파일의 연산 결과를 제공하는 서비스입니다.

## 🛠️ 사용 기술
- **프론트엔드**: HTML, CSS (SB Admin 2 템플릿 사용)
- **백엔드**: Python (Flask)
- **데이터 처리**: Google Sheets API

## 📂 프로젝트 구조
```
📁 프로젝트 폴더
├── 📄 app.py
├── 📁 templates/
│   ├── 📄 index.html
└── 📄 README.md
```

## 🚀 실행 방법
### 1️⃣ 저장소 클론
```bash
git clone https://github.com/sewon-2/Mandatory-Renewable-Energy-Installation.git
cd Mandatory-Renewable-Energy-Installation
```
### 2️⃣ 가상 환경 설정 및 패키지 설치
```bash
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```
### 3️⃣ Flask 서버 실행
```bash
python app.py
```   
### 4️⃣ 웹 브라우저에서 실행
[http://127.0.0.1:5000/](http://127.0.0.1:5000/) 접속하여 서비스 확인
