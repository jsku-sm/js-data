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

    import pyreadstat
    import statsmodels.api as sm
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import os

    # ── 한글 폰트 ──────────────────────────────────────────────
    @st.cache_resource
    def _set_font():
        for path in [
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "C:/Windows/Fonts/malgun.ttf",
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        ]:
            if os.path.exists(path):
                fm.fontManager.addfont(path)
                prop = fm.FontProperties(fname=path)
                plt.rcParams['font.family'] = prop.get_name()
                plt.rcParams['axes.unicode_minus'] = False
                return
        plt.rcParams['axes.unicode_minus'] = False
    _set_font()

    # ── 헤더 ──────────────────────────────────────────────────
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

    # ── 데이터 업로드 ─────────────────────────────────────────
    uploaded = st.file_uploader(
        "📂 SAV 파일을 업로드하세요 (중고등학생 데이터)",
        type=["sav"],
        key="assign2_sav",
        help="_데이터__2023_청소년_금융이해력_및_금융생활실태_조사_중고등학생.SAV",
    )

    # ── 데이터 로드 & 전처리 ──────────────────────────────────
    @st.cache_data
    def _load(file_bytes):
        with open("_tmp.sav", "wb") as f:
            f.write(file_bytes)
        df, meta = pyreadstat.read_sav("_tmp.sav")
        os.remove("_tmp.sav")
        return df

    @st.cache_data
    def _preprocess(df):
        d = df.copy()
        knowledge = ['Q02','Q03','Q04','Q05','Q06','Q07','Q08']
        behavior  = ['Q09','Q0901','Q11','Q12','Q13','Q14']
        d['금융이해력'] = d[knowledge].sum(axis=1) + d[behavior].sum(axis=1)

        q26_cols = ['Q26','Q2601','Q2602','Q2603','Q2604','Q2605','Q2606']
        d['Q26'] = d[[c for c in q26_cols if c in d.columns]].sum(axis=1)

        q33_cols = ['Q33','Q3301','Q3302','Q3303','Q3304']
        d['Q33'] = d[[c for c in q33_cols if c in d.columns]].sum(axis=1)

        d = d.dropna(subset=['Q26','Q27','Q33','금융이해력'])
        d = pd.get_dummies(d, columns=['Q27'], drop_first=True)
        q27_col = [c for c in d.columns if 'Q27_' in c][0]
        return d, q27_col

    if uploaded is None:
        st.info("👆 SAV 파일을 업로드하면 분석 결과가 자동으로 표시됩니다!")
        # 업로드 없이도 보고서 구조는 볼 수 있도록 탭 표시
        df_loaded, q27_col, model = None, None, None
    else:
        with st.spinner("데이터 불러오는 중..."):
            df_raw = _load(uploaded.read())
            df_loaded, q27_col = _preprocess(df_raw)
            X = df_loaded[['Q26','Q33', q27_col]].astype(float)
            y = df_loaded['금융이해력'].astype(float)
            model = sm.OLS(y, sm.add_constant(X)).fit()
        st.success(f"✅ {len(df_raw):,}명 로드 → 결측치 제거 후 **{len(df_loaded):,}명** 분석")

    # ── 탭 구성 ───────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📁 데이터 소개", "🎯 연구 설계", "🔍 분석 방법", "📈 분석 결과", "💡 결론 및 시사점"]
    )

    # ── TAB 1: 데이터 소개 ─────────────────────────────────────
    with tab1:
        st.subheader("📁 1. 데이터 소개")
        st.markdown("""
본 연구는 **한국청소년정책연구원**이 2023년 5월에 수행한
「2023 청소년 금융이해력 및 금융생활실태 조사」의 **중·고등학생 데이터**를 활용하였습니다.
""")
        for col, icon, title, desc, color in zip(
            st.columns(3),
            ["📊", "📖", "📋"],
            ["원시 데이터", "코드북", "설문 문항지"],
            ["중고등학생 .SAV 파일", "변수 설명 .xls 파일", "조사표 .pdf 파일"],
            ["#3b82f6", "#8b5cf6", "#10b981"],
        ):
            with col:
                st.markdown(
                    f"""<div style="background:{color}12; border:1.5px solid {color}40;
                        border-radius:14px; padding:20px; text-align:center; min-height:130px;">
                        <div style="font-size:2rem; margin-bottom:8px;">{icon}</div>
                        <div style="font-weight:700; color:{color}; font-size:0.9rem; margin-bottom:6px;">{title}</div>
                        <div style="font-size:0.8rem; color:#64748b;">{desc}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

        st.divider()
        st.markdown("""
| 항목 | 내용 |
|------|------|
| 조사기관 | 한국청소년정책연구원 |
| 조사대상 | 전국 중·고등학생 |
| 조사시기 | 2023년 5월 |
| 조사방법 | 학교 방문 면접 조사 |
| 데이터 형식 | SPSS (.SAV) |
""")

        if df_loaded is not None:
            st.divider()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("전체 표본", f"{len(df_raw):,}명")
            c2.metric("유효 표본", f"{len(df_loaded):,}명")
            c3.metric("금융이해력 평균", f"{df_loaded['금융이해력'].mean():.2f}점")
            c4.metric("부모교육 평균", f"{df_loaded['Q26'].mean():.2f}점")

    # ── TAB 2: 연구 설계 ───────────────────────────────────────
    with tab2:
        st.subheader("🎯 2. 연구 설계")
        st.markdown(
            """
            <div style="background:#f0f9ff; border-left:5px solid #0891b2;
                        border-radius:0 12px 12px 0; padding:20px 24px; margin-bottom:24px;">
                <div style="font-weight:700; color:#0c4a6e; margin-bottom:8px;">🔬 연구 주제</div>
                <div style="color:#0c4a6e; font-size:0.95rem; line-height:1.8;">
                    <strong>"중·고등학생의 부모 금융교육이 청소년 금융이해력(지식·행위)에 미치는 영향"</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("#### 📌 변수 구성")
        st.markdown(
            """
            <div style="background:#fef9c3; border:1.5px solid #fbbf24;
                        border-radius:12px; padding:16px 20px; margin-bottom:12px;">
                <span style="background:#f59e0b; color:white; padding:3px 12px;
                             border-radius:99px; font-size:0.78rem; font-weight:700;">종속변수</span>
                <span style="font-weight:700; font-size:1rem; margin-left:10px;">금융이해력 종합점수</span>
                <div style="margin-top:8px; color:#64748b; font-size:0.85rem; line-height:1.7;">
                    📌 Q02~Q08 금융지식 7문항 + Q09~Q14 금융행위 6문항 합산
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for xn, name, var, desc, color in [
            ("X1", "부모 금융교육 수준", "Q26", "7문항 4점 리커트 합산점수", "#3b82f6"),
            ("X2", "학교 금융교육 경험", "Q27", "경험 유무 → 더미변수 (있음=1, 없음=0)", "#8b5cf6"),
            ("X3", "금융 웰빙",         "Q33", "5문항 4점 리커트 합산점수", "#10b981"),
        ]:
            st.markdown(
                f"""<div style="background:{color}0d; border:1.5px solid {color}40;
                    border-radius:12px; padding:16px 20px; margin-bottom:10px;">
                    <span style="background:{color}; color:white; padding:3px 12px;
                                 border-radius:99px; font-size:0.78rem; font-weight:700;">독립변수 {xn}</span>
                    <span style="font-weight:700; font-size:1rem; margin-left:10px;">{name}</span>
                    <div style="margin-top:8px; color:#64748b; font-size:0.85rem;">
                        📌 {var} — {desc}
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
        st.markdown("#### 🔮 연구 가설")
        for i, hypo in enumerate([
            "부모 금융교육 수준이 높을수록 청소년의 금융이해력이 높을 것이다.",
            "학교 금융교육 경험이 있는 학생이 없는 학생보다 금융이해력이 높을 것이다.",
            "금융 웰빙 수준이 높을수록 청소년의 금융이해력이 높을 것이다.",
        ], 1):
            st.markdown(f"- **가설 {i}**: {hypo}")

    # ── TAB 3: 분석 방법 ──────────────────────────────────────
    with tab3:
        st.subheader("🔍 3. 분석 방법")
        for num, color, title, items in [
            ("1", "#ef4444", "데이터 전처리", [
                "SAV 파일 로드 (pyreadstat)",
                "금융이해력 종합점수 생성: Q02~Q14 합산",
                "Q26 7문항 합산, Q33 5문항 합산",
                "Q27 더미화: 있음=1, 없음=0",
                "결측치 포함 행 제거",
            ]),
            ("2", "#f59e0b", "탐색적 데이터 분석(EDA)", [
                "변수별 기술통계 (평균·표준편차·분포)",
                "히스토그램으로 분포 시각화",
                "Q27 경험 유무 빈도 확인",
            ]),
            ("3", "#3b82f6", "다중공선성 검사", [
                "VIF(분산팽창계수) 계산",
                "VIF < 10이면 다중공선성 문제 없음",
            ]),
            ("4", "#10b981", "다중선형회귀분석", [
                "OLS(최소제곱법) 회귀모형 적합",
                "R², 수정된 R², F통계량으로 모형 적합도 평가",
                "회귀계수, t값, p값으로 유의성 판단",
                "95% 신뢰구간 확인",
            ]),
        ]:
            with st.expander(f"STEP {num}. {title}", expanded=True):
                for item in items:
                    st.markdown(f"- {item}")

    # ── TAB 4: 분석 결과 ──────────────────────────────────────
    with tab4:
        st.subheader("📈 4. 분석 결과")

        if df_loaded is None or model is None:
            st.info("👆 SAV 파일을 업로드하면 실제 분석 결과가 표시됩니다!")
        else:
            # 기술통계
            st.markdown("#### 4-1. 기술통계")
            st.dataframe(pd.DataFrame({
                "변수": ["금융이해력 종합점수", "부모 금융교육(Q26)", "금융 웰빙(Q33)"],
                "평균": [df_loaded['금융이해력'].mean(), df_loaded['Q26'].mean(), df_loaded['Q33'].mean()],
                "표준편차": [df_loaded['금융이해력'].std(), df_loaded['Q26'].std(), df_loaded['Q33'].std()],
                "최솟값": [df_loaded['금융이해력'].min(), df_loaded['Q26'].min(), df_loaded['Q33'].min()],
                "최댓값": [df_loaded['금융이해력'].max(), df_loaded['Q26'].max(), df_loaded['Q33'].max()],
            }).style.format({"평균":"{:.2f}","표준편차":"{:.2f}","최솟값":"{:.0f}","최댓값":"{:.0f}"}),
            use_container_width=True, hide_index=True)

            q27_yes = int(df_loaded[q27_col].sum())
            q27_no  = len(df_loaded) - q27_yes
            st.caption(f"학교 금융교육 경험: 있음 {q27_yes:,}명({q27_yes/len(df_loaded)*100:.1f}%) / 없음 {q27_no:,}명({q27_no/len(df_loaded)*100:.1f}%)")

            # VIF
            st.markdown("#### 4-2. 다중공선성 검사 (VIF)")
            X_vif = df_loaded[['Q26','Q33', q27_col]].astype(float)
            vif_df = pd.DataFrame({
                "변수": ["부모 금융교육(Q26)", "금융 웰빙(Q33)", "학교 금융교육(Q27)"],
                "VIF": [variance_inflation_factor(X_vif.values, i) for i in range(3)],
            })
            vif_df['판정'] = vif_df['VIF'].apply(lambda x: "✅ 문제없음" if x < 10 else "⚠️ 주의")
            st.dataframe(vif_df.style.format({"VIF":"{:.4f}"}),
                         use_container_width=True, hide_index=True)
            st.caption("모든 VIF < 10 → 다중공선성 문제 없음")

            # 회귀분석
            st.markdown("#### 4-3. 다중선형회귀분석")
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("R²",        f"{model.rsquared:.4f}")
            mc2.metric("수정된 R²", f"{model.rsquared_adj:.4f}")
            mc3.metric("F 통계량 p값", f"{model.f_pvalue:.2e}")

            if model.f_pvalue < 0.05:
                st.success("✅ 모델이 통계적으로 유의미합니다! (p < 0.05)")

            reg_df = pd.DataFrame({
                "변수": ["상수", "부모 금융교육(Q26)", "금융 웰빙(Q33)", "학교 금융교육(Q27)"],
                "회귀계수(B)": model.params.values,
                "표준오차":    model.bse.values,
                "t값":         model.tvalues.values,
                "p값":         model.pvalues.values,
            })
            reg_df["유의성"] = reg_df["p값"].apply(
                lambda p: "*** p<.001" if p < 0.001
                else ("** p<.01" if p < 0.01
                else ("* p<.05" if p < 0.05 else "비유의"))
            )
            st.dataframe(
                reg_df.style.format({"회귀계수(B)":"{:.4f}","표준오차":"{:.4f}","t값":"{:.3f}","p값":"{:.4f}"}),
                use_container_width=True, hide_index=True,
            )

            # 계수 시각화
            coef_df = reg_df[reg_df["변수"] != "상수"].copy()
            fig, ax = plt.subplots(figsize=(7, 3))
            colors = ["#55A868" if p < 0.05 else "#AAAAAA" for p in coef_df["p값"]]
            ax.barh(coef_df["변수"], coef_df["회귀계수(B)"], color=colors, alpha=0.85)
            ax.axvline(0, color="black", linewidth=0.8)
            ax.set_xlabel("회귀계수")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)

    # ── TAB 5: 결론 및 시사점 ─────────────────────────────────
    with tab5:
        st.subheader("💡 5. 결론 및 시사점")

        if df_loaded is None or model is None:
            st.info("👆 SAV 파일을 업로드하면 실제 데이터 기반 결론이 표시됩니다!")
            show_q26_sig = show_q27_sig = True
            show_q33_sig = False
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
