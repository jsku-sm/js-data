"""
페이지 1 — 내 소개
"""

import streamlit as st


def render():

    # ── 헤더 배너 ──────────────────────────────────────────────────
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 16px;
            padding: 48px 40px;
            margin-bottom: 32px;
            text-align: center;
        ">
            <div style="
                width: 100px; height: 100px;
                border-radius: 50%;
                background: linear-gradient(135deg, #4a9eff, #a855f7);
                margin: 0 auto 20px;
                display: flex; align-items: center; justify-content: center;
                font-size: 48px; line-height: 100px;
            ">🎓</div>
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
        value="""■ 컴퓨터공학 학사 / 수학교육 석사 / AI융합교육 석사과정

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

    # ── 포트폴리오 사진 업로드 ────────────────────────────────────
    st.divider()
    st.subheader("🖼️ 포트폴리오 사진 업로드")
    uploaded = st.file_uploader(
        "프로필 사진 또는 프로젝트 스크린샷을 업로드하세요 (PNG/JPG)",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
    )
    if uploaded:
        img_cols = st.columns(min(len(uploaded), 4))
        for i, img in enumerate(uploaded):
            with img_cols[i % 4]:
                st.image(img, caption=img.name, use_container_width=True)
    else:
        st.info("📁 사진을 업로드하면 여기에 표시됩니다.")
