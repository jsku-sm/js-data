"""
페이지 1 — 내 소개
"""

import streamlit as st
import base64
from pathlib import Path


def _img_to_base64(img_path: str) -> str:
    """이미지 파일을 base64 문자열로 변환"""
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render():

    # ── 프로필 이미지 base64 변환 ──────────────────────────────────
    img_path = Path(__file__).parent.parent / "images" / "profile.jpg"
    if img_path.exists():
        img_b64 = _img_to_base64(str(img_path))
        profile_html = f"""
            <div style="
                width: 120px; height: 120px;
                border-radius: 50%;
                overflow: hidden;
                margin: 0 auto 20px;
                border: 4px solid #4a9eff;
                box-shadow: 0 0 20px rgba(74,158,255,0.4);
            ">
                <img src="data:image/jpeg;base64,{img_b64}"
                     style="width:100%; height:100%; object-fit:cover;" />
            </div>
        """
    else:
        profile_html = """
            <div style="
                width: 120px; height: 120px;
                border-radius: 50%;
                background: linear-gradient(135deg, #4a9eff, #a855f7);
                margin: 0 auto 20px;
                display: flex; align-items: center; justify-content: center;
                font-size: 48px; line-height: 120px;
            ">🎓</div>
        """

    # ── 헤더 배너 ──────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 16px;
            padding: 48px 40px;
            margin-bottom: 32px;
            text-align: center;
        ">
            {profile_html}
            <h1 style="color: white; font-size: 2.2rem; margin: 0 0 8px; font-weight: 700;">
                구정숙
            </h1>
            <p style="color: #94a3b8; font-size: 1.1rem; margin: 0 0 16px;">
                AI융합교육전공 학번 : 2542100
            </p>
            <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
                <span style="background:#1e3a5f; color:#60a5fa; padding:6px 16px; border-radius:99px; font-size:0.85rem;">📍 숙명여자대학교</span>
                <span style="background:#1e3a5f; color:#60a5fa; padding:6px 16px; border-radius:99px; font-size:0.85rem;">📧 scatchi@sookimyung.ac.kr</span>
                <span style="background:#1e3a5f; color:#60a5fa; padding:6px 16px; border-radius:99px; font-size:0.85rem;">🐙 </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 자기소개 ───────────────────────────────────────────────────
    st.subheader("👋 About me")
    intro_text = st.text_area(
        "자기소개를 입력하세요",
        value="""■ 저는

26년 가까이 교단에 서며
학생들이 언제 진짜로 배우는가를 고민해왔습니다.

학생의 사고력과 개념적 이해를 이끌어내는 수업을 실천하고 있으며 질문하고, 탐구하고, 기록을 통해
성장하는 과정 중심 수업을 지향합니다.""",
        height=200,
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

    contact_card(c1, "📧", "이메일",   "scatchi@sookimyung.ac.kr", "#3b82f6")
    contact_card(c2, "🐙", "GitHub",   "",                          "#8b5cf6")
    contact_card(c3, "💼", "LinkedIn", "",                          "#0ea5e9")
    contact_card(c4, "📝", "블로그",   "blog.example.com",          "#10b981")

    # ── 단체 사진 ─────────────────────────────────────────────────
    st.divider()
    community_path = Path(__file__).parent.parent / "images" / "community.jpg"
    if community_path.exists():
        st.markdown(
            """
            <h3 style="text-align:center; margin-bottom:12px;">
                📸 함께 연구하며 성장하는 경복 디지털 선도교사 공동체
            </h3>
            """,
            unsafe_allow_html=True,
        )
        st.image(str(community_path), use_container_width=True)
