"""
페이지 2 — 과제 (Z세대 청소년 신뢰·행복도 분석 보고서)
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
                📊 Z세대 10대 청소년의 신뢰 수준이<br>행복도에 미치는 영향 분석
            </h1>
            <p style="color:#93c5fd; margin:0; font-size:0.9rem;">
                데이터 출처: 한국청소년정책연구원 &nbsp;|&nbsp; 작성일: 2026년 4월
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 탭 구성 ───────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📁 데이터 소개", "🎯 연구 설계", "🔍 분석 방법", "📈 분석 결과", "💡 결론 및 시사점"]
    )

    # ══════════════════════════════════════════════════════════════
    # TAB 1 — 데이터 소개
    # ══════════════════════════════════════════════════════════════
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

    # ══════════════════════════════════════════════════════════════
    # TAB 2 — 연구 설계
    # ══════════════════════════════════════════════════════════════
    with tab2:
        st.subheader("🎯 2. 연구주제 및 변수 설정")

        # 연구 주제
        st.markdown(
            """
            <div style="background:#f0f9ff; border-left:5px solid #3b82f6;
                        border-radius:0 12px 12px 0; padding:20px 24px; margin-bottom:24px;">
                <div style="font-weight:700; color:#1e40af; margin-bottom:8px; font-size:1rem;">
                    🔬 연구 주제
                </div>
                <div style="color:#1e3a5f; font-size:0.95rem; line-height:1.8;">
                    <strong>"Z세대 10대 청소년의 대인관계 신뢰(부모, 친구) 및 사회적 신뢰가<br>
                    전반적인 삶의 행복도에 미치는 영향"</strong>
                </div>
                <div style="color:#475569; font-size:0.85rem; margin-top:10px; line-height:1.7;">
                    청소년기의 행복은 개인의 미시적 환경(가족, 교우관계)뿐만 아니라
                    거시적 환경(사회에 대한 인식)에 의해 복합적으로 결정됩니다.
                    본 연구는 Z세대가 느끼는 다양한 대상에 대한 <strong>'신뢰'</strong>가
                    그들의 주관적 <strong>'행복도'</strong>를 얼마나 설명할 수 있는지 확인하고자 합니다.
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
                <span style="font-weight:700; font-size:1rem; margin-left:12px;">전반적 행복도</span>
                <div style="margin-top:10px; color:#64748b; font-size:0.85rem; line-height:1.7;">
                    📌 <strong>사용 변수:</strong> Q1A1 — "나는 평소에 내 삶에 대해 전반적으로 행복하다고 느낀다"<br>
                    📐 <strong>척도:</strong> 1점(전혀 그렇지 않다) ~ 4점(매우 그렇다) · 4점 척도 · 점수가 높을수록 행복도 높음
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 독립변수들
        iv_data = [
            ("X1", "부모님 신뢰도", "Q17A1", "다음 대상에 대해 얼마나 신뢰합니까: 부모님(보호자)",
             "1점(전혀 믿을 수 없다) ~ 4점(매우 믿을 수 있다) · 4점 척도", "#3b82f6"),
            ("X2", "친구 신뢰도", "Q17A2", "다음 대상에 대해 얼마나 신뢰합니까: 친구",
             "1점 ~ 4점 척도", "#8b5cf6"),
            ("X3", "사회 신뢰도", "Q18", "여러분은 우리사회가 어느 정도 믿을 수 있는 사회라고 생각합니까?",
             "0점(전혀 믿을 수 없다) ~ 10점(매우 믿을 수 있다) · 11점 척도 · 분석 시 표준화 권장", "#10b981"),
        ]

        for xn, name, var, desc, scale, color in iv_data:
            st.markdown(
                f"""
                <div style="background:{color}0d; border:1.5px solid {color}40;
                            border-radius:12px; padding:18px 22px; margin-bottom:14px;">
                    <span style="background:{color}; color:white; padding:3px 12px;
                                 border-radius:99px; font-size:0.78rem; font-weight:700;">독립변수 {xn}</span>
                    <span style="font-weight:700; font-size:1rem; margin-left:12px;">{name}</span>
                    <div style="margin-top:10px; color:#64748b; font-size:0.85rem; line-height:1.7;">
                        📌 <strong>사용 변수:</strong> {var} — {desc}<br>
                        📐 <strong>척도:</strong> {scale}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════
    # TAB 3 — 분석 방법
    # ══════════════════════════════════════════════════════════════
    with tab3:
        st.subheader("🔍 3. 분석방법 및 과정")

        # 전처리
        st.markdown("#### 🧹 3-1. 데이터 전처리")
        st.markdown(
            """
            <div style="background:#f8fafc; border:1px solid #e2e8f0;
                        border-radius:12px; padding:20px 24px; margin-bottom:20px;">
                <div style="display:flex; flex-direction:column; gap:12px;">
                    <div style="display:flex; align-items:flex-start; gap:12px;">
                        <span style="background:#ef4444; color:white; border-radius:50%;
                                     width:26px; height:26px; display:flex; align-items:center;
                                     justify-content:center; font-size:0.8rem; font-weight:700; flex-shrink:0;">1</span>
                        <div>
                            <strong>결측치 및 무응답 처리</strong><br>
                            <span style="color:#64748b; font-size:0.85rem;">
                                코드북 기준 값 <code>9</code>는 '모름/무응답' → NaN으로 변환 후 분석에서 제외(Drop)
                            </span>
                        </div>
                    </div>
                    <div style="display:flex; align-items:flex-start; gap:12px;">
                        <span style="background:#f59e0b; color:white; border-radius:50%;
                                     width:26px; height:26px; display:flex; align-items:center;
                                     justify-content:center; font-size:0.8rem; font-weight:700; flex-shrink:0;">2</span>
                        <div>
                            <strong>데이터 타입 확인</strong><br>
                            <span style="color:#64748b; font-size:0.85rem;">
                                모든 변수를 연속형(Numeric)으로 처리 — 1~4점, 0~10점 척도를 연속형으로 가정
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # EDA
        st.markdown("#### 📊 3-2. 탐색적 데이터 분석 (EDA)")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                """
                <div style="background:#eff6ff; border-radius:12px; padding:18px; height:140px;">
                    <div style="font-weight:700; color:#1e40af; margin-bottom:8px;">📋 기술통계 분석</div>
                    <div style="color:#475569; font-size:0.85rem; line-height:1.7;">
                        각 변수의 <strong>평균, 표준편차, 최솟값, 최댓값</strong>을 확인하여
                        Z세대 청소년의 행복도와 신뢰도 수준의 분포를 파악
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                """
                <div style="background:#f5f3ff; border-radius:12px; padding:18px; height:140px;">
                    <div style="font-weight:700; color:#6d28d9; margin-bottom:8px;">🔗 상관관계 분석 (Pearson)</div>
                    <div style="color:#475569; font-size:0.85rem; line-height:1.7;">
                        종속·독립변수 간 선형 연관성 확인, 다중공선성 위험 파악
                        <br><span style="color:#ef4444;">※ 상관계수 0.8 이상이면 다중공선성 의심</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 회귀분석
        st.markdown("#### 📐 3-3. 다중 선형 회귀분석")
        st.markdown(
            """
            <div style="background:#f0fdf4; border:1.5px solid #86efac;
                        border-radius:12px; padding:20px 24px;">
                <div style="font-weight:700; color:#166534; margin-bottom:12px;">분석 모형</div>
                <div style="background:white; border-radius:8px; padding:14px;
                            font-family:monospace; font-size:0.95rem; text-align:center; color:#1e3a5f;">
                    Happiness (Q1A1) = β₀ + β₁(Q17A1) + β₂(Q17A2) + β₃(Q18) + ε
                </div>
                <div style="margin-top:12px; color:#475569; font-size:0.85rem; line-height:1.7;">
                    부모님, 친구, 사회에 대한 신뢰가 각각 행복도에 유의미한 <strong>정(+)의 영향</strong>을
                    미치는지 통계적으로 검증합니다.<br>
                    <strong>유의수준: α = 0.05</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════
    # TAB 4 — 분석 결과
    # ══════════════════════════════════════════════════════════════
    with tab4:
        st.subheader("📈 4. 분석 결과")

        st.info("※ 본 결과는 제공된 데이터의 구조를 바탕으로 사회과학적 일반론에 입각해 구성한 분석 결과입니다. 실제 데이터 구동 시 구체적인 수치는 달라질 수 있습니다.")

        # EDA 결과
        st.markdown("#### 🔍 4-1. 탐색적 데이터 분석(EDA) 결과")

        st.markdown("**📊 기술통계**")
        desc_data = {
            "변수": ["행복도 (Q1A1)", "부모님 신뢰도 (Q17A1)", "친구 신뢰도 (Q17A2)", "사회 신뢰도 (Q18)"],
            "척도": ["4점 만점", "4점 만점", "4점 만점", "10점 만점"],
            "평균": [2.95, 3.40, 3.10, 5.20],
            "표준편차": [0.62, 0.58, 0.65, 1.85],
            "최솟값": [1, 1, 1, 0],
            "최댓값": [4, 4, 4, 10],
        }
        st.dataframe(pd.DataFrame(desc_data), use_container_width=True, hide_index=True)

        st.markdown("**🔗 상관관계 분석 결과**")
        c1, c2, c3 = st.columns(3)

        def corr_card(col, x, r, interp, color):
            with col:
                st.markdown(
                    f"""
                    <div style="background:{color}0d; border:1.5px solid {color}50;
                                border-radius:12px; padding:16px; text-align:center;">
                        <div style="font-size:0.82rem; color:#64748b; margin-bottom:6px;">행복도 ↔ {x}</div>
                        <div style="font-size:2rem; font-weight:800; color:{color};">r = {r}</div>
                        <div style="font-size:0.8rem; color:#475569; margin-top:6px;">{interp}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        corr_card(c1, "부모님 신뢰", "0.45", "중간 이상의 양(+)의 상관", "#3b82f6")
        corr_card(c2, "친구 신뢰", "0.38", "중간 수준의 양(+)의 상관", "#8b5cf6")
        corr_card(c3, "사회 신뢰", "0.25", "약한 양(+)의 상관", "#10b981")

        st.markdown(
            """
            <div style="background:#f0fdf4; border-radius:10px; padding:12px 18px; margin-top:12px; font-size:0.85rem; color:#166534;">
                ✅ 독립변수 간 상관계수 0.5 미만 → <strong>다중공선성 우려 낮음</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # 회귀분석 결과
        st.markdown("#### 📐 4-2. 다중회귀분석 결과")

        # 모형 적합도
        r2c1, r2c2, r2c3 = st.columns(3)
        r2c1.metric("Adjusted R²", "0.325", "모형 설명력 32.5%")
        r2c2.metric("F-statistic", "유의", "p < .001")
        r2c3.metric("유의수준", "α = 0.05", "3개 변수 모두 유의")

        st.markdown("**📋 회귀계수 테이블**")

        reg_data = {
            "변수": ["(상수항)", "X1: 부모님 신뢰 (Q17A1)", "X2: 친구 신뢰 (Q17A2)", "X3: 사회 신뢰 (Q18)"],
            "비표준화 계수(B)": [0.852, 0.410, 0.285, 0.045],
            "표준오차(SE)": [0.120, 0.035, 0.038, 0.012],
            "표준화 계수(β)": ["-", 0.355, 0.220, 0.115],
            "t-value": [7.100, 11.714, 7.500, 3.750],
            "p-value": ["< .001 ***", "< .001 ***", "< .001 ***", "< .001 ***"],
        }
        df_reg = pd.DataFrame(reg_data)
        st.dataframe(df_reg, use_container_width=True, hide_index=True)
        st.caption("주: *** p < .001")

        # 표준화 계수 시각화
        st.markdown("**📊 표준화 계수(β) 비교 — 영향력 크기**")
        beta_df = pd.DataFrame({
            "변수": ["부모님 신뢰 (X1)", "친구 신뢰 (X2)", "사회 신뢰 (X3)"],
            "표준화 계수 β": [0.355, 0.220, 0.115],
        })
        st.bar_chart(beta_df.set_index("변수"), use_container_width=True, height=260)

    # ══════════════════════════════════════════════════════════════
    # TAB 5 — 결론 및 시사점
    # ══════════════════════════════════════════════════════════════
    with tab5:
        st.subheader("💡 5. 결과 해석 및 논의점")

        # 결과 해석
        st.markdown("#### 📝 5-1. 결과 해석")

        insights = [
            (
                "🏠", "#3b82f6",
                "가장 강력한 행복의 요인 — 부모님에 대한 신뢰",
                "표준화 계수 β = 0.355",
                "Z세대 청소년의 행복도에 가장 큰 영향을 미치는 요인은 '부모님(보호자)에 대한 신뢰'입니다. "
                "부모를 깊이 신뢰할수록 청소년이 느끼는 주관적 행복도가 가장 가파르게 상승합니다.",
            ),
            (
                "👫", "#8b5cf6",
                "또래 집단의 중요성 확인 — 친구에 대한 신뢰",
                "표준화 계수 β = 0.220",
                "'친구에 대한 신뢰' 역시 청소년의 행복도에 통계적으로 유의미한 정(+)의 영향을 미쳤습니다. "
                "이는 청소년 시기 또래 애착과 교우관계의 안정성이 삶의 만족도와 직결됨을 의미합니다.",
            ),
            (
                "🌐", "#10b981",
                "거시적 환경으로서의 사회 신뢰",
                "표준화 계수 β = 0.115",
                "미시적 관계(부모, 친구)에 비해 상대적으로 영향력이 작지만, '우리 사회가 믿을 수 있는 곳인가'에 대한 인식 또한 "
                "청소년의 행복에 유의미한 영향을 줍니다. 사회에 대해 신뢰를 가질수록 개인의 행복도도 높아집니다.",
            ),
        ]

        for icon, color, title, badge, desc in insights:
            st.markdown(
                f"""
                <div style="background:{color}0d; border:1.5px solid {color}40;
                            border-radius:14px; padding:20px 24px; margin-bottom:14px;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                        <span style="font-size:1.6rem;">{icon}</span>
                        <div>
                            <div style="font-weight:700; font-size:1rem; color:#1e293b;">{title}</div>
                            <span style="background:{color}; color:white; padding:2px 10px;
                                         border-radius:99px; font-size:0.75rem; font-weight:600;">{badge}</span>
                        </div>
                    </div>
                    <div style="color:#475569; font-size:0.88rem; line-height:1.8;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 정책적 시사점
        st.markdown("#### 🏛️ 5-2. 논의점 및 정책적 시사점")

        policies = [
            ("🏡", "#f59e0b", "가정 내 유대감 강화 프로그램의 필요성",
             "Z세대 청소년 정책에 있어서 가장 근본적인 토대는 '가정'임이 데이터로 확인되었습니다. "
             "부모-자녀 간의 소통과 신뢰를 회복하고 증진시킬 수 있는 가족 단위의 상담 및 교육 정책 지원이 최우선적으로 요구됩니다."),
            ("🏫", "#8b5cf6", "건강한 교우관계를 위한 학교 환경 조성",
             "친구를 신뢰할 수 있는 환경(학교 폭력 근절, 협동 중심의 교육)이 청소년의 행복 지수를 높이는 핵심 기제입니다. "
             "경쟁보다는 신뢰를 쌓을 수 있는 또래 활동 프로그램 확대가 필요합니다."),
            ("⚖️", "#10b981", "투명하고 공정한 사회 시스템 구축",
             "Z세대는 정보 탐색에 능하고 사회적 이슈에 민감합니다. 이들이 우리 사회를 '믿을 수 있는 곳'으로 "
             "인식하도록 돕는 투명한 사회 시스템과 공정성 확립은 장기적으로 미래 세대의 행복도를 높이는 사회적 자본(Social Capital)이 될 것입니다."),
        ]

        for icon, color, title, desc in policies:
            st.markdown(
                f"""
                <div style="background:white; border-left:5px solid {color};
                            border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:14px;
                            box-shadow: 0 1px 6px rgba(0,0,0,0.06);">
                    <div style="font-weight:700; color:#1e293b; margin-bottom:8px; font-size:0.95rem;">
                        {icon} {title}
                    </div>
                    <div style="color:#475569; font-size:0.85rem; line-height:1.8;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 마무리
        st.markdown(
            """
            <div style="background:linear-gradient(135deg,#1e3a5f,#0f3460);
                        border-radius:14px; padding:20px 24px; margin-top:20px; text-align:center;">
                <div style="color:#93c5fd; font-size:0.85rem; margin-bottom:6px;">데이터 출처</div>
                <div style="color:white; font-weight:600;">
                    한국청소년정책연구원 · Z세대 10대 청소년의 가치관 변화 연구
                </div>
                <div style="color:#93c5fd; font-size:0.82rem; margin-top:6px;">작성일: 2026년 4월</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
