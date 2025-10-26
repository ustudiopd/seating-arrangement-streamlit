# 🏫 자리배치 Streamlit 앱

HTML 기반 자리배치 프로그램을 Streamlit으로 변환한 웹 애플리케이션입니다.

## ✨ 주요 기능

- 📝 **학생 명단 관리**: 텍스트 입력으로 간편한 명단 등록
- 🏗️ **다양한 배치 옵션**: 기본형, 짝꿍형(분단형) 배치 지원
- 🎯 **고급 자리 배치**: 랜덤 배치, 사전 지정, 자리 띄우기 기능
- 👁️ **시각적 결과**: 교사/학생 기준 보기 전환 가능
- 📊 **엑셀 내보내기**: 자리 배치 결과를 엑셀 파일로 다운로드
- 💾 **데이터 영속성**: JSON 파일로 설정 저장/불러오기

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/ustudiopd/seating-arrangement-streamlit.git
cd seating-arrangement-streamlit
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 앱 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하여 사용할 수 있습니다.

## 📖 사용법

### 기본 사용법
1. **명단 입력**: 학생 이름을 한 줄에 한 명씩 입력
2. **배치 설정**: 원하는 책상 배열 유형과 크기 설정
3. **자리 배치**: '자리 바꾸기!' 버튼으로 랜덤 배치 생성
4. **결과 확인**: 교사/학생 기준으로 보기 전환 가능
5. **엑셀 저장**: 결과를 엑셀 파일로 다운로드

### 고급 기능
- **사전 자리 지정**: 특정 학생을 원하는 자리에 고정
- **자리 띄우기**: 선택한 학생들이 서로 붙어 앉지 않도록 설정
- **데이터 저장**: 설정을 JSON 파일로 저장하여 나중에 불러오기 가능

## 🏗️ 프로젝트 구조

```
├── app.py                    # 메인 Streamlit 애플리케이션
├── requirements.txt          # 의존성 패키지 목록
├── README.md                # 프로젝트 설명
├── utils/                   # 유틸리티 모듈
│   ├── seating_algorithm.py # 자리 배치 알고리즘
│   ├── excel_export.py     # 엑셀 다운로드 기능
│   └── data_manager.py     # 데이터 저장/불러오기
└── memory_bank/            # 메모리 뱅크 문서들
```

## 🛠️ 기술 스택

- **Python 3.8+**
- **Streamlit**: 웹 애플리케이션 프레임워크
- **Pandas**: 데이터 처리
- **OpenPyXL**: 엑셀 파일 생성
- **NumPy**: 수치 계산

## 📋 요구사항

- Python 3.8 이상
- pip 패키지 매니저

## 🤝 기여하기

1. 이 저장소를 포크합니다
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이나 버그 리포트는 [Issues](https://github.com/ustudiopd/seating-arrangement-streamlit/issues) 페이지를 통해 제출해주세요.

---

**Made with ❤️ by ustudiopd**