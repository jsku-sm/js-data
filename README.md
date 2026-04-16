# 🎓 나의 포트폴리오 — Streamlit 멀티페이지 앱

## 📁 파일 구조

```
streamlit_app/
├── app.py                  ← 메인 진입점 (여기서 실행)
├── requirements.txt        ← 의존 패키지
└── pages/
    ├── __init__.py
    ├── intro.py            ← 🏠 내 소개 페이지
    ├── assignment.py       ← 📚 과제 관리 페이지
    └── analysis.py         ← 📊 데이터 분석 페이지
```

## 🚀 실행 방법

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 앱 실행
streamlit run app.py
```

브라우저에서 http://localhost:8501 이 자동으로 열립니다.

## 📌 페이지별 기능

### 🏠 내 소개
- 프로필 배너 (이름, 소속, 연락처)
- 자기소개 텍스트 에디터
- 기술 스택 뱃지
- 관심 분야 프로그레스 바
- 주요 활동 타임라인
- 포트폴리오 사진 업로드

### 📚 과제 관리
- 과제 등록 폼 (과목·제목·마감일·우선순위·상태)
- 검색 & 필터 (상태/우선순위)
- D-day 카운터 자동 계산
- 파일 첨부 기능
- 상태 실시간 변경 & 삭제
- CSV 내보내기

### 📊 데이터 분석
- CSV / Excel 파일 업로드 or 샘플 데이터
- 데이터 탐색 (미리보기, 컬럼 정보, 결측값)
- 시각화 (막대·선·산점도·히스토그램·범주 분포)
- 통계 분석 (기술통계, 상관분석, 그룹별 집계)
- CSV 내보내기 & 분석 메모 저장

## 🛠 Streamlit 주요 컴포넌트

| 컴포넌트 | 사용 위치 |
|---|---|
| `st.sidebar`, `st.radio` | 전체 네비게이션 |
| `st.text_input`, `st.text_area` | 자기소개, 메모 |
| `st.progress`, `st.metric` | 관심분야, KPI 지표 |
| `st.file_uploader` | 사진·CSV·Excel 업로드 |
| `st.form`, `st.form_submit_button` | 과제 등록 폼 |
| `st.dataframe`, `st.table` | 데이터 테이블 |
| `st.line_chart`, `st.bar_chart`, `st.scatter_chart` | 차트 시각화 |
| `st.tabs`, `st.expander`, `st.columns` | 레이아웃 |
| `st.download_button` | CSV 다운로드 |
| `st.session_state` | 과제·데이터 상태 유지 |
| `@st.cache_data` | 샘플 데이터 캐싱 |
