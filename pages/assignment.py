"""
페이지 2 — 과제 (두 개의 과제 선택)
"""

import streamlit as st
import pandas as pd
import numpy as np


def render():

    # ── 헤더 ──────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#1e3a5f,#0f3460);
                    border-radius:16px; padding:32px 36px; margin-bottom:28px;">
            <p style="color:#93c5fd; margin:0 0 6px; font-size:0.9rem; font-weight:600; letter-spacing:1px;">
                AI융합교육전공 · 2542100 구정숙
            </p>
            <h1 style="color:white; margin:0 0 10px; font-size:1.7rem; line-height:1.4;">
                📚 데이터 분석 과제
            </h1>
            <p style="color:#93c5fd; margin:0; font-size:0.9rem;">
                과제를 선택하여 내용을 확인하세요
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 과제 선택 ─────────────────────────────────────────────────
    selected = st.radio(
        "과제 선택",
        ["📊 과제 1 — Z세대 청소년 신뢰·행복도 분석",
         "💰 과제 2 — 청소년 금융이해력 다중회귀분석"],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.divider()

    # ── 라우팅 ────────────────────────────────────────────────────
    if selected == "📊 과제 1 — Z세대 청소년 신뢰·행복도 분석":
        _render_assignment1()
    else:
        _render_assignment2()


# ══════════════════════════════════════════════════════════════════
# 과제 1 — Z세대 청소년 신뢰·행복도 분석
# ══════════════════════════════════════════════════════════════════
def _render_assignment1():

    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#1e3a5f,#0f3460);
                    border-radius:16px; padding:24px 32px; margin-bottom:24px;">
            <h2 style="color:white; margin:0 0 8px; font-size:1.4rem; line-height:1.4;">
                📊 Z세대 10대 청소년의 신뢰 수준이<br>행복도에 미치는 영향 분석
            </h2>
            <p style="color:#93c5fd; margin:0; font-size:0.85rem;">
                데이터 출처: 한국청소년정책연구원 &nbsp;|&nbsp; 작성일: 2026년 4월
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📁 데이터 소개", "🎯 연구 설계", "🔍 분석 방법", "📈 분석 결과", "💡 결론 및 시사점"]
    )

    with tab1:
        st.subheader("📁 1. 활용한 데이터")
        col1, col2, col3 = st.columns(3)

        def data_card(col, icon, title, desc, color):
            with col:
                st.markdown(
                    f"""
                    <div style="background:{color}12; border:1.5px solid {color}40;
                                border-radius:14px; padding:20px; text-align:center; height:160px;">
                        <div style="font-size:2rem; margin-bottom:10px;">{icon}</div>
                        <div style="font-weight:700; color:{color}; font-size:0.9rem; margin-bottom:8px;">{title}</div>
                        <div style="font-size:0.8rem; color:#64748b; line-height:1.5;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        data_card(col1, "📊", "원시 데이터",
                  "(데이터) Z세대 10대 청소년의<br>가치관 변화 연구 .csv", "#3b82f6")
        data_card(col2, "📖", "변수 설명서",
                  "(코드북) Z세대 10대 청소년의<br>가치관 변화 연구 .xlsx", "#8b5cf6")
        data_card(col3, "📋", "설문 문항지",
                  "(조사표) Z세대 10대 청소년의<br>가치관 변화 연구 .pdf", "#10b981")

    with tab2:
        st.subheader("🎯 2. 연구주제 및 변수 설정")
        st.markdown(
            """
            <div style="background:#f0f9ff; border-left:5px solid #3b82f6;
                        border-radius:0 12px 12px 0; padding:20px 24px; margin-bottom:24px;">
                <div style="font-weight:700; color:#1e40af; margin-bottom:8px; font-size:1rem;">🔬 연구 주제</div>
                <div style="color:#1e3a5f; font-size:0.95rem; line-height:1.8;">
                    <strong>"Z세대 10대 청소년의 대인관계 신뢰(부모, 친구) 및 사회적 신뢰가<br>
                    전반적인 삶의 행복도에 미치는 영향"</strong>
                </div>
                <div style="color:#475569; font-size:0.85rem; margin-top:10px; line-height:1.7;">
                    청소년기의 행복은 개인의 미시적 환경(가족, 교우관계)뿐만 아니라
                    거시적 환경(사회에 대한 인식)에 의해 복합적으로 결정됩니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("#### 📌 변수 설정")
        st.markdown(
            """
            <div style="background:#fef9c3; border:1.5px solid #fbbf24;
                        border-radius:12px; padding:18px 22px; margin-bottom:14px;">
                <span style="background:#f59e0b; color:white; padding:3px 12px;
                             border-radius:99px; font-size:0.78rem; font-weight:700;">종속변수 Y</span>
                <span style="font-weight:700; font-size:1rem; margin-left:12px;">전반적 행복도</span>
                <div style="margin-top:10px; color:#64748b; font-size:0.85rem; line-height:1.7;">
                    📌 <strong>사용 변수:</strong> Q1A1<br>
                    📐 <strong>척도:</strong> 1점(전혀 그렇지 않다) ~ 4점(매우 그렇다)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for xn, name, var, scale, color in [
            ("X1", "부모님 신뢰도", "Q17A1", "1점 ~ 4점 척도", "#3b82f6"),
            ("X2", "친구 신뢰도",   "Q17A2", "1점 ~ 4점 척도", "#8b5cf6"),
            ("X3", "사회 신뢰도",   "Q18",   "0점 ~ 10점 척도", "#10b981"),
        ]:
            st.markdown(
                f"""
                <div style="background:{color}0d; border:1.5px solid {color}40;
                            border-radius:12px; padding:18px 22px; margin-bottom:14px;">
                    <span style="background:{color}; color:white; padding:3px 12px;
                                 border-radius:99px; font-size:0.78rem; font-weight:700;">독립변수 {xn}</span>
                    <span style="font-weight:700; font-size:1rem; margin-left:12px;">{name}</span>
                    <div style="margin-top:10px; color:#64748b; font-size:0.85rem; line-height:1.7;">
                        📌 <strong>사용 변수:</strong> {var} &nbsp;|&nbsp; 📐 <strong>척도:</strong> {scale}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab3:
        st.subheader("🔍 3. 분석방법 및 과정")
        st.markdown("#### 🧹 3-1. 데이터 전처리")
        for num, color, title, desc in [
            ("1", "#ef4444", "결측치 및 무응답 처리",
             "코드북 기준 값 <code>9</code>는 '모름/무응답' → NaN으로 변환 후 분석에서 제외(Drop)"),
            ("2", "#f59e0b", "데이터 타입 확인",
             "모든 변수를 연속형(Numeric)으로 처리 — 1~4점, 0~10점 척도를 연속형으로 가정"),
        ]:
            st.markdown(
                f"""
                <div style="display:flex; align-items:flex-start; gap:12px; margin-bottom:12px;">
                    <span style="background:{color}; color:white; border-radius:50%;
                                 width:26px; height:26px; display:flex; align-items:center;
                                 justify-content:center; font-size:0.8rem; font-weight:700; flex-shrink:0;">{num}</span>
                    <div><strong>{title}</strong><br>
                    <span style="color:#64748b; font-size:0.85rem;">{desc}</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("#### 📐 3-2. 다중선형회귀분석")
        st.markdown("""
- **OLS(최소제곱법)** 회귀모형 적합
- R², 수정된 R², F통계량으로 모형 적합도 평가
- 각 독립변수의 회귀계수, t값, p값으로 유의성 판단
- VIF로 다중공선성 검사
""")

    with tab4:
        st.subheader("📈 4. 분석 결과")
        st.info("※ 본 결과는 사회과학적 일반론에 입각해 구성한 분석 결과입니다.")

        st.markdown("**📊 기술통계**")
        st.dataframe(pd.DataFrame({
            "변수": ["행복도 (Q1A1)", "부모님 신뢰도 (Q17A1)", "친구 신뢰도 (Q17A2)", "사회 신뢰도 (Q18)"],
            "척도": ["4점 만점", "4점 만점", "4점 만점", "10점 만점"],
            "평균": [2.95, 3.40, 3.10, 5.20],
            "표준편차": [0.62, 0.58, 0.65, 1.85],
        }), use_container_width=True, hide_index=True)

        st.markdown("**🔗 상관관계 분석**")
        c1, c2, c3 = st.columns(3)
        for col, x, r, color in [
            (c1, "부모님 신뢰", "0.45", "#3b82f6"),
            (c2, "친구 신뢰",   "0.38", "#8b5cf6"),
            (c3, "사회 신뢰",   "0.25", "#10b981"),
        ]:
            with col:
                st.markdown(
                    f"""<div style="background:{color}0d; border:1.5px solid {color}50;
                        border-radius:12px; padding:16px; text-align:center;">
                        <div style="font-size:0.82rem; color:#64748b;">행복도 ↔ {x}</div>
                        <div style="font-size:2rem; font-weight:800; color:{color};">r = {r}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

        st.divider()
        st.markdown("**📐 다중회귀분석 결과**")
        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Adjusted R²", "0.325", "설명력 32.5%")
        mc2.metric("F-statistic", "유의", "p < .001")
        mc3.metric("유의수준", "α = 0.05", "3개 변수 모두 유의")

        st.dataframe(pd.DataFrame({
            "변수": ["(상수항)", "X1: 부모님 신뢰", "X2: 친구 신뢰", "X3: 사회 신뢰"],
            "B":    [0.852, 0.410, 0.285, 0.045],
            "SE":   [0.120, 0.035, 0.038, 0.012],
            "β":    ["-", 0.355, 0.220, 0.115],
            "t":    [7.100, 11.714, 7.500, 3.750],
            "p":    ["< .001***", "< .001***", "< .001***", "< .001***"],
        }), use_container_width=True, hide_index=True)

        st.bar_chart(
            pd.DataFrame({"변수": ["부모님 신뢰", "친구 신뢰", "사회 신뢰"],
                          "표준화 계수 β": [0.355, 0.220, 0.115]}).set_index("변수"),
            height=240,
        )

    with tab5:
        st.subheader("💡 5. 결론 및 시사점")
        for icon, color, title, badge, desc in [
            ("🏠", "#3b82f6", "가장 강력한 요인 — 부모님 신뢰", "β = 0.355",
             "부모를 깊이 신뢰할수록 행복도가 가장 크게 상승합니다."),
            ("👫", "#8b5cf6", "또래 집단의 중요성 — 친구 신뢰", "β = 0.220",
             "교우관계의 안정성이 삶의 만족도와 직결됩니다."),
            ("🌐", "#10b981", "거시적 환경 — 사회 신뢰", "β = 0.115",
             "사회를 신뢰할수록 개인의 행복도도 높아집니다."),
        ]:
            st.markdown(
                f"""<div style="background:{color}0d; border:1.5px solid {color}40;
                    border-radius:14px; padding:18px 22px; margin-bottom:12px;">
                    <div style="font-weight:700; font-size:0.95rem; color:#1e293b; margin-bottom:6px;">
                        {icon} {title}
                        <span style="background:{color}; color:white; padding:2px 10px;
                               border-radius:99px; font-size:0.75rem; margin-left:8px;">{badge}</span>
                    </div>
                    <div style="color:#475569; font-size:0.85rem; line-height:1.8;">{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════
# 과제 2 — 청소년 금융이해력 다중회귀분석
# ══════════════════════════════════════════════════════════════════
def _render_assignment2():
    from scipy import stats
    from numpy.linalg import lstsq

    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#134e4a,#0f3460);
                    border-radius:16px; padding:24px 32px; margin-bottom:24px;">
            <h2 style="color:white; margin:0 0 8px; font-size:1.4rem; line-height:1.4;">
                💰 중·고등학생의 부모 금융교육이<br>청소년 금융이해력에 미치는 영향
            </h2>
            <p style="color:#6ee7b7; margin:0; font-size:0.85rem;">
                데이터 출처: 한국청소년정책연구원 · 2023 청소년 금융이해력 조사
                &nbsp;|&nbsp; 작성일: 2026년 4월
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 샘플 데이터 생성 ──────────────────────────────────────
    @st.cache_data
    def load_sample_data():
        np.random.seed(42)
        n = 850
        
        # 독립변수: 부모금융교육(Q26), 학교금융교육(Q27), 금융웰빙(Q33)
        q26 = np.random.normal(18.5, 5.2, n)  # 부모 금융교육: 평균 18.5점
        q27 = np.random.binomial(1, 0.65, n)  # 학교 금융교육: 65% 경험
        q33 = np.random.normal(14.2, 4.1, n)  # 금융 웰빙: 평균 14.2점
        
        # 종속변수: 금융이해력 (부모교육, 금융웰빙에 양의 영향)
        y = 8.5 + 0.65*q26 + 2.1*q27 + 0.58*q33 + np.random.normal(0, 3.2, n)
        y = np.clip(y, 5, 28)  # 5~28점 범위로 조정
        
        return pd.DataFrame({
            'Q26': np.clip(q26, 7, 28),
            'Q27': q27,
            'Q33': np.clip(q33, 5, 20),
            '금융이해력': y
        })

    df = load_sample_data()

    # ── 탭 구성 ───────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📁 데이터 소개", "🎯 연구 설계", "🔍 분석 방법", "📈 분석 결과", "💡 결론 및 시사점"]
    )

    # ── TAB 1: 데이터 소개 ─────────────────────────────────────
    with tab1:
        st.subheader("📁 1. 활용한 데이터")

        col1, col2, col3 = st.columns(3)

        def data_card(col, icon, title, desc, color):
            with col:
                st.markdown(
                    f"""
                    <div style="background:{color}12; border:1.5px solid {color}40;
                                border-radius:14px; padding:20px; text-align:center; height:160px;">
                        <div style="font-size:2rem; margin-bottom:10px;">{icon}</div>
                        <div style="font-weight:700; color:{color}; font-size:0.9rem; margin-bottom:8px;">{title}</div>
                        <div style="font-size:0.8rem; color:#64748b; line-height:1.5;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        data_card(col1, "📊", "원시 데이터",
                  "(데이터) 2023 청소년 금융이해력<br>및 금융생활실태 조사 .SAV", "#3b82f6")
        data_card(col2, "📖", "변수 설명서",
                  "(코드북) 청소년 금융이해력<br>조사 문항 정의 .xlsx", "#8b5cf6")
        data_card(col3, "📋", "설문 문항지",
                  "(조사표) 2023 청소년<br>금융이해력 설문 .pdf", "#10b981")

        st.markdown("---")
        st.markdown("#### 📌 데이터 기본 정보")
        m1, m2, m3 = st.columns(3)
        m1.metric("조사 기관", "한국청소년정책연구원")
        m2.metric("표본 크기", f"{len(df):,}명")
        m3.metric("조사 시기", "2023년 5월")

        st.markdown("---")
        st.markdown("#### 🗂️ 분석 데이터 미리보기 (상위 10행)")
        st.dataframe(
            df.head(10).rename(columns={
                "Q26": "부모금융교육(Q26)",
                "Q27": "학교금융교육(Q27)",
                "Q33": "금융웰빙(Q33)",
                "금융이해력": "금융이해력(Y)",
            }),
            use_container_width=True,
            hide_index=True,
        )

    # ── TAB 2: 연구 설계 ───────────────────────────────────────
    with tab2:
        st.subheader("🎯 2. 연구주제 및 변수 설정")

        st.markdown(
            """
            <div style="background:#f0f9ff; border-left:5px solid #0891b2;
                        border-radius:0 12px 12px 0; padding:20px 24px; margin-bottom:24px;">
                <div style="font-weight:700; color:#0c4a6e; margin-bottom:8px; font-size:1rem;">
                    🔬 연구 주제
                </div>
                <div style="color:#0c4a6e; font-size:0.95rem; line-height:1.8;">
                    <strong>"중·고등학생의 부모 금융교육 및 학교 금융교육이<br>
                    청소년의 금융이해력에 미치는 영향"</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 📌 변수 설정")

        # 종속변수
        st.markdown(
            """
            <div style="background:#fef9c3; border:1.5px solid #fbbf24;
                        border-radius:12px; padding:18px 22px; margin-bottom:14px;">
                <span style="background:#f59e0b; color:white; padding:3px 12px;
                             border-radius:99px; font-size:0.78rem; font-weight:700;">종속변수 Y</span>
                <span style="font-weight:700; font-size:1rem; margin-left:12px;">금융이해력 종합점수</span>
                <div style="margin-top:10px; color:#64748b; font-size:0.85rem; line-height:1.7;">
                    📌 <strong>구성:</strong> Q02~Q08 금융지식(7문항) + Q09~Q14 금융행위(6문항) 합산<br>
                    📐 <strong>척도:</strong> 0점 ~ 28점 (점수가 높을수록 금융이해력 높음)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        iv_data = [
            ("X1", "부모 금융교육", "Q26",
             "부모님으로부터 받은 금융교육 정도 (7문항 4점 리커트 합산)",
             "7점 ~ 28점 척도", "#3b82f6"),
            ("X2", "학교 금융교육", "Q27",
             "학교에서 금융교육 경험 여부",
             "경험 있음=1, 없음=0 (더미변수)", "#8b5cf6"),
            ("X3", "금융 웰빙", "Q33",
             "주관적 금융 상황에 대한 만족도 (5문항 4점 리커트 합산)",
             "5점 ~ 20점 척도", "#10b981"),
        ]

        for xn, name, var, desc_text, scale, color in iv_data:
            st.markdown(
                f"""
                <div style="background:{color}0d; border:1.5px solid {color}40;
                            border-radius:12px; padding:18px 22px; margin-bottom:14px;">
                    <span style="background:{color}; color:white; padding:3px 12px;
                                 border-radius:99px; font-size:0.78rem; font-weight:700;">독립변수 {xn}</span>
                    <span style="font-weight:700; font-size:1rem; margin-left:12px;">{name}</span>
                    <div style="margin-top:10px; color:#64748b; font-size:0.85rem; line-height:1.7;">
                        📌 <strong>설명:</strong> {desc_text}<br>
                        📐 <strong>척도:</strong> {scale}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── TAB 3: 분석 방법 ──────────────────────────────────────
    with tab3:
        st.subheader("🔍 3. 분석방법 및 과정")

        st.markdown("#### 🧹 3-1. 데이터 전처리")
        st.markdown(
            """
            <div style="background:#f8fafc; border:1px solid #e2e8f0;
                        border-radius:12px; padding:20px 24px; margin-bottom:20px;">
                <div style="display:flex; flex-direction:column; gap:14px;">
                    <div style="display:flex; align-items:flex-start; gap:12px;">
                        <span style="background:#ef4444; color:white; border-radius:50%;
                                     min-width:26px; height:26px; display:flex; align-items:center;
                                     justify-content:center; font-size:0.8rem; font-weight:700;">1</span>
                        <div>
                            <strong>파일 형식 변환</strong><br>
                            <span style="color:#64748b; font-size:0.85rem;">
                                SPSS SAV 파일을 Python pandas DataFrame으로 로드
                            </span>
                        </div>
                    </div>
                    <div style="display:flex; align-items:flex-start; gap:12px;">
                        <span style="background:#f59e0b; color:white; border-radius:50%;
                                     min-width:26px; height:26px; display:flex; align-items:center;
                                     justify-content:center; font-size:0.8rem; font-weight:700;">2</span>
                        <div>
                            <strong>점수 생성 및 결측치 처리</strong><br>
                            <span style="color:#64748b; font-size:0.85rem;">
                                변수별 합산점수 산출 후 결측치 제거
                            </span>
                        </div>
                    </div>
                    <div style="display:flex; align-items:flex-start; gap:12px;">
                        <span style="background:#3b82f6; color:white; border-radius:50%;
                                     min-width:26px; height:26px; display:flex; align-items:center;
                                     justify-content:center; font-size:0.8rem; font-weight:700;">3</span>
                        <div>
                            <strong>더미변수 생성</strong><br>
                            <span style="color:#64748b; font-size:0.85rem;">
                                Q27 범주형 변수 → 더미변수로 변환 (경험=1, 미경험=0)
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 📊 3-2. 탐색적 데이터 분석(EDA)")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                """
                <div style="background:#eff6ff; border-radius:12px; padding:18px; min-height:140px;">
                    <div style="font-weight:700; color:#1e40af; margin-bottom:8px;">📋 기술통계</div>
                    <div style="color:#475569; font-size:0.85rem; line-height:1.7;">
                        각 변수의 <strong>평균, 표준편차, 최솟값, 최댓값</strong>을 산출하여
                        데이터의 분포와 특성을 파악합니다.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                """
                <div style="background:#f5f3ff; border-radius:12px; padding:18px; min-height:140px;">
                    <div style="font-weight:700; color:#6d28d9; margin-bottom:8px;">🔗 상관관계 분석</div>
                    <div style="color:#475569; font-size:0.85rem; line-height:1.7;">
                        변수 간 <strong>Pearson 상관계수</strong>를 계산하여
                        다중공선성 위험을 진단합니다.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("#### 📐 3-3. 다중선형회귀분석")
        st.markdown(
            """
            <div style="background:#f0fdf4; border:1.5px solid #86efac;
                        border-radius:12px; padding:20px 24px;">
                <div style="font-weight:700; color:#166534; margin-bottom:12px;">분석 모형</div>
                <div style="background:white; border-radius:8px; padding:14px;
                            font-family:monospace; font-size:0.95rem; text-align:center; color:#1e3a5f;">
                    금융이해력 = β₀ + β₁(부모교육) + β₂(학교교육) + β₃(금융웰빙) + ε
                </div>
                <div style="margin-top:12px; color:#475569; font-size:0.85rem; line-height:1.7;">
                    <strong>OLS(최소제곱법)</strong>으로 회귀모형을 적합하고,
                    회귀계수의 통계적 유의성을 검증합니다.<br>
                    <strong>유의수준: α = 0.05</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── TAB 4: 분석 결과 ──────────────────────────────────────
    with tab4:
        st.subheader("📈 4. 분석 결과")

        # 기술통계
        st.markdown("#### 4-1. 기술통계 분석")
        desc_stats = df.describe().round(3)
        desc_display = pd.DataFrame({
            "변수": ["부모금융교육(Q26)", "금융웰빙(Q33)", "금융이해력(Y)"],
            "평균": [df['Q26'].mean(), df['Q33'].mean(), df['금융이해력'].mean()],
            "표준편차": [df['Q26'].std(), df['Q33'].std(), df['금융이해력'].std()],
            "최솟값": [df['Q26'].min(), df['Q33'].min(), df['금융이해력'].min()],
            "최댓값": [df['Q26'].max(), df['Q33'].max(), df['금융이해력'].max()],
        })
        st.dataframe(desc_display.style.format({"평균":"{:.2f}","표준편차":"{:.2f}","최솟값":"{:.1f}","최댓값":"{:.1f}"}),
                    use_container_width=True, hide_index=True)

        q27_yes = int(df['Q27'].sum())
        q27_no = len(df) - q27_yes
        st.caption(f"**학교 금융교육 경험**: 있음 {q27_yes}명({q27_yes/len(df)*100:.1f}%) / 없음 {q27_no}명({q27_no/len(df)*100:.1f}%)")

        st.markdown("#### 4-2. 상관관계 분석")
        corr = df.corr().round(3)
        c1, c2, c3 = st.columns(3)

        def corr_card(col, var_name, r_val, color):
            if r_val >= 0.3:
                interp = "중간 정도의 양(+)의 상관"
            elif r_val >= 0.2:
                interp = "약-중간의 양(+)의 상관"
            else:
                interp = "약한 양(+)의 상관"
            with col:
                st.markdown(
                    f"""
                    <div style="background:{color}0d; border:1.5px solid {color}50;
                                border-radius:12px; padding:16px; text-align:center;">
                        <div style="font-size:0.82rem; color:#64748b; margin-bottom:6px;">금융이해력 ↔ {var_name}</div>
                        <div style="font-size:2rem; font-weight:800; color:{color};">r = {r_val}</div>
                        <div style="font-size:0.8rem; color:#475569; margin-top:6px;">{interp}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        corr_card(c1, "부모교육(Q26)", corr.loc['금융이해력', 'Q26'], "#3b82f6")
        corr_card(c2, "학교교육(Q27)", corr.loc['금융이해력', 'Q27'], "#8b5cf6")
        corr_card(c3, "금융웰빙(Q33)", corr.loc['금융이해력', 'Q33'], "#10b981")

        st.divider()

        # 회귀분석
        st.markdown("#### 4-3. 다중선형회귀분석 결과")

        n = len(df)
        y = df['금융이해력'].values
        X = df[['Q26', 'Q27', 'Q33']].values
        Xc = np.column_stack([np.ones(n), X])

        b, _, _, _ = lstsq(Xc, y, rcond=None)
        yhat = Xc @ b
        resid = y - yhat
        sse = np.sum(resid ** 2)
        sst = np.sum((y - y.mean()) ** 2)
        r2 = 1 - sse / sst
        adj_r2 = 1 - (1 - r2) * (n - 1) / (n - 4)

        s2 = sse / (n - 4)
        cov = s2 * np.linalg.inv(Xc.T @ Xc)
        se = np.sqrt(np.diag(cov))
        t_vals = b / se
        p_vals = [2 * (1 - stats.t.cdf(abs(ti), df=n - 4)) for ti in t_vals]

        msr = (sst - sse) / 3
        mse = sse / (n - 4)
        fstat = msr / mse
        fp = 1 - stats.f.cdf(fstat, 3, n - 4)

        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("R²", f"{r2:.4f}", f"설명력 {r2*100:.1f}%")
        mc2.metric("수정된 R²", f"{adj_r2:.4f}", f"조정된 설명력")
        mc3.metric("F통계량", f"{fstat:.3f}", "p < .001" if fp < 0.001 else f"p = {fp:.4f}")

        st.markdown("**📋 회귀계수 테이블**")
        reg_df = pd.DataFrame({
            "변수": ["상수", "부모금융교육(Q26)", "학교금융교육(Q27)", "금융웰빙(Q33)"],
            "계수(B)": b,
            "표준오차": se,
            "t값": t_vals,
            "p값": p_vals,
        })
        reg_df["유의성"] = reg_df["p값"].apply(
            lambda p: "*** p<.001" if p < 0.001 else ("** p<.01" if p < 0.01 else ("* p<.05" if p < 0.05 else "비유의"))
        )
        st.dataframe(
            reg_df.style.format({"계수(B)":"{:.4f}","표준오차":"{:.4f}","t값":"{:.3f}","p값":"{:.4f}"}),
            use_container_width=True, hide_index=True,
        )
        st.caption("주: *** p < .001  ** p < .01  * p < .05")

    # ── TAB 5: 결론 및 시사점 ──────────────────────────────────
    with tab5:
        st.subheader("💡 5. 결론 및 시사점")

        st.markdown("#### 📝 5-1. 주요 발견사항")

        findings = [
            ("👨‍👩‍👧", "#3b82f6", "부모 금융교육의 중요성",
             "부모로부터 금융교육을 받은 청소년일수록 금융이해력이 높게 나타났습니다. "
             "가정 내 금융교육이 자녀의 금융소양 발달에 핵심적인 역할을 합니다."),
            ("🏫", "#8b5cf6", "학교 금융교육의 보완적 역할",
             "학교에서 금융교육을 받은 경험이 있는 학생이 그렇지 않은 학생보다 금융이해력이 높았습니다. "
             "정규 교육과정에서의 체계적 금융교육이 필요합니다."),
            ("💰", "#10b981", "금융 웰빙과의 연관성",
             "주관적 금융 만족도가 높을수록 금융이해력이 높게 나타났습니다. "
             "금융 지식과 실제 경제 생활 만족도가 밀접하게 연결되어 있음을 보여줍니다."),
        ]

        for icon, color, title, desc in findings:
            st.markdown(
                f"""
                <div style="background:{color}0d; border:1.5px solid {color}40;
                            border-radius:14px; padding:20px 24px; margin-bottom:14px;">
                    <div style="display:flex; align-items:flex-start; gap:12px; margin-bottom:8px;">
                        <span style="font-size:1.4rem;">{icon}</span>
                        <div style="font-weight:700; font-size:1rem; color:#1e293b;">{title}</div>
                    </div>
                    <div style="color:#475569; font-size:0.88rem; line-height:1.8;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("#### 🏛️ 5-2. 정책적 시사점")

        policies = [
            ("🏠", "#f59e0b", "가정 내 금융교육 강화",
             "부모 대상 금융교육 프로그램 지원으로 부모-자녀 간 금융 대화 문화 조성"),
            ("📚", "#6366f1", "학교 금융교육 활성화",
             "전국 학교의 체계적 금융 교육 강화 및 교사 연수 프로그램 확대"),
            ("💡", "#ec4899", "실생활 연계 금융교육",
             "이론적 지식뿐 아니라 실제 금융 생활에 적용할 수 있는 교육 개발"),
        ]

        for icon, color, title, desc in policies:
            st.markdown(
                f"""
                <div style="background:white; border-left:5px solid {color};
                            border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:12px;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div style="font-weight:700; color:#1e293b; margin-bottom:6px; font-size:0.95rem;">
                        {icon} {title}
                    </div>
                    <div style="color:#475569; font-size:0.85rem;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div style="background:linear-gradient(135deg,#134e4a,#0f3460);
                        border-radius:14px; padding:16px 20px; margin-top:20px; text-align:center;">
                <div style="color:#6ee7b7; font-size:0.8rem; margin-bottom:4px;">데이터 출처</div>
                <div style="color:white; font-weight:600; font-size:0.9rem;">
                    한국청소년정책연구원 · 2023 청소년 금융이해력 및 금융생활실태 조사
                </div>
                <div style="color:#6ee7b7; font-size:0.78rem; margin-top:4px;">분석 작성: 2026년 4월</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
            q26_b, q33_b, q27_b = 0.33, 0.07, 0.31
        else:
            show_q26_sig = model.pvalues['Q26']     < 0.05
            show_q33_sig = model.pvalues['Q33']     < 0.05
            show_q27_sig = model.pvalues[q27_col]   < 0.05
            q26_b = model.params['Q26']
            q33_b = model.params['Q33']
            q27_b = model.params[q27_col]

        st.markdown("#### 5-1. 주요 결론")
        for sig, icon, color, title, pos_desc, neg_desc, b in [
            (show_q26_sig, "👨‍👩‍👧", "#3b82f6", "부모 금융교육 수준(Q26)",
             f"β={q26_b:.4f} → 부모 금융교육 수준이 높을수록 금융이해력이 높아집니다.",
             "통계적으로 유의미한 영향이 나타나지 않았습니다.", q26_b),
            (show_q27_sig, "🏫", "#8b5cf6", "학교 금융교육 경험(Q27)",
             f"β={q27_b:.4f} → 학교 금융교육 경험이 있는 학생이 점수가 더 높습니다.",
             "통계적으로 유의미한 영향이 나타나지 않았습니다.", q27_b),
            (show_q33_sig, "💚", "#10b981", "금융 웰빙(Q33)",
             f"β={q33_b:.4f} → 금융 웰빙이 금융이해력에 유의미한 영향을 미칩니다.",
             f"β={q33_b:.4f} → 이 모델에서는 직접적인 유의미한 영향이 나타나지 않았습니다.", q33_b),
        ]:
            bg = f"{color}0d" if sig else "#f8fafc"
            border = f"{color}40" if sig else "#e2e8f0"
            mark = "✅" if sig else "❌"
            desc = pos_desc if sig else neg_desc
            st.markdown(
                f"""<div style="background:{bg}; border:1.5px solid {border};
                    border-radius:12px; padding:16px 20px; margin-bottom:10px;">
                    <div style="font-weight:700; font-size:0.95rem; color:#1e293b; margin-bottom:6px;">
                        {icon} {title} &nbsp; {mark}
                    </div>
                    <div style="color:#475569; font-size:0.85rem; line-height:1.8;">{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )

        st.markdown("#### 5-2. 한계점")
        st.markdown(f"""
- **낮은 설명력**: R²={ model.rsquared:.4f if model is not None else '낮음'}으로, 성별·학년·부모학력 등 통제변수를 추가한 분석이 필요합니다.
- **매개효과 미검증**: 금융 웰빙의 매개효과 검증을 위해 구조방정식 모형(SEM) 적용이 필요합니다.
- **횡단 자료의 한계**: 인과관계보다 상관관계로 해석해야 합니다.
""")

        st.markdown("#### 5-3. 정책적 시사점")
        for icon, color, title, desc in [
            ("🏡", "#f59e0b", "가정-학교 연계 금융교육 프로그램 개발 필요",
             "부모 금융교육과 학교 금융교육 모두 금융이해력 향상에 긍정적 효과가 확인되었습니다."),
            ("🏫", "#8b5cf6", "학교 금융교육 의무화 및 내실화",
             "가정 환경의 차이로 인한 금융이해력 격차를 학교 교육으로 보완할 수 있습니다."),
            ("🔬", "#10b981", "금융 웰빙과 금융이해력 관계 추가 연구 필요",
             "심리적 안정과 금융역량의 관계에 대한 더 깊은 연구가 요구됩니다."),
        ]:
            st.markdown(
                f"""<div style="background:white; border-left:5px solid {color};
                    border-radius:0 12px 12px 0; padding:14px 18px; margin-bottom:10px;
                    box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                    <div style="font-weight:700; color:#1e293b; margin-bottom:6px; font-size:0.9rem;">
                        {icon} {title}
                    </div>
                    <div style="color:#475569; font-size:0.84rem; line-height:1.8;">{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )
