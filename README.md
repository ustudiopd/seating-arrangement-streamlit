# 자리배치 Streamlit 앱

기존 HTML 기반 자리배치 프로그램을 Streamlit으로 변환한 웹 애플리케이션입니다.

## 기능

- 학생 명단 입력 및 파일 기반 저장/불러오기
- 책상 배열 설정 (기본형, 짝꿍형)
- 자리 배치 알고리즘 (랜덤 배치, 사전 지정, 자리 띄우기)
- 교사/학생 기준 보기 전환
- 엑셀 다운로드 기능

## 설치 및 실행

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 앱 실행:
```bash
streamlit run app.py
```

## 프로젝트 구조

```
├── app.py                 # 메인 Streamlit 애플리케이션
├── requirements.txt       # 의존성 패키지 목록
├── utils/                 # 유틸리티 모듈
│   ├── seating_algorithm.py  # 자리 배치 알고리즘
│   ├── excel_export.py      # 엑셀 다운로드 기능
│   └── data_manager.py      # 데이터 저장/불러오기
└── README.md             # 프로젝트 설명
```
