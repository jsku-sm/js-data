"""
메인 앱 — 페이지 네비게이션 진입점
실행: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="데이타 분석 과제",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 상단 자동 페이지 네비게이션 바 숨기기 ──
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── 공통 사이드바 ──
with st.sidebar:
    st.markdown("## 🎓 데이타분석")
    st.caption("AI융합교육전공 2542100 구정숙")
    st.divider()

    page = st.radio(
        "페이지 선택",
        ["🏠 내 소개", "📚 과제", "📊 데이터 분석"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("© 2026 구쌤's")

# ── 페이지 라우팅 ──
if page == "🏠 내 소개":
    from pages.intro import render
    render()
elif page == "📚 과제":
    from pages.assignment import render
    render()
elif page == "📊 데이터 분석":
    from pages.analysis import render
    render()