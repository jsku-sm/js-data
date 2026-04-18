"""
페이지 1 — 내 소개
"""

import streamlit as st
import base64
from pathlib import Path


def _img_to_base64(img_path: str) -> str:
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render():

    # ── 프로필 이미지 + About me 2단 레이아웃 ──────────────────────
    img_path = Path(__file__).parent.parent / "images" / "profile.jpg"

    col_img, col_text = st.columns([1, 2], gap="large")

    with col_img:
        if img_path.exists():
            img_b64 = _img_to_base64(str(img_path))
            st.markdown(
                f"""
                <div style="display:flex; justify-content:center; align-items:center; height:100%;">
                    <img src="data:image/jpeg;base64,{img_b64}"
                         style="width:100%; max-width:280px; border-radius:16px;" />
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown("🎓", unsafe_allow_html=True)

    with col_text:
        st.markdown(
            """
            <div style="padding-top: 8px;">
                <h1 style="font-size:2rem; font-weight:700; margin:0 0 4px;">구정숙</h1>
                <p style="color:#64748b; font-size:1rem; margin:0 0 16px;">
                    AI융합교육전공 &nbsp;|&nbsp; 학번 2542100
                </p>
                <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px;">
                    <span style="background:#eff6ff; color:#3b82f6; padding:5px 14px; border-radius:99px; font-size:0.85rem;">📍 숙명여자대학교</span>
                    <span style="background:#eff6ff; color:#3b82f6; padding:5px 14px; border-radius:99px; font-size:0.85rem;">📧 scatchi@sookimyung.ac.kr</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("👋 About me")
        st.text_area(
            "자기소개",
            value="""■ 컴퓨터공학 학사 / 수학교육 석사 / AI융합교육 석사과정

학생의 사고력과 개념적 이해를 이끌어내는 수업을 실천하고 있으며
질문하고, 탐구하고, 기록을 통해 성장하는 과정 중심 수업을 지향합니다.

#의미 중심 사고 #F 감성 + T 논리의 공존 #섬세함 vs 예민함
#감정의 깊이 #이지적 긴장감인간적인 허점
""",
            height=180,
            label_visibility="collapsed",
        )

    # ── 연락처 카드 ───────────────────────────────────────────────
    st.divider()
    st.subheader("📬 연락처 & SNS")
    c1, c2, c3, c4 = st.columns(4)

    def contact_card(col, icon, label, value, color):
        with col:
            st.markdown(
                f"""<div style="background:{color}18; border:1px solid {color}44;
                    border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:1.8rem;">{icon}</div>
                    <div style="font-size:0.78rem; color:#64748b; margin:4px 0;">{label}</div>
                    <div style="font-weight:600; font-size:0.9rem; color:{color};">{value}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    contact_card(c1, "📧", "이메일", "scatchi@sookimyung.ac.kr", "#3b82f6")
    contact_card(c2, "💼", "인스타", "https://www.instagram.com/gussam@", "#0ea5e9")
    contact_card(c3, "📝", "블로그", "https://blog.naver.com/scatchi", "#ec4899")
   