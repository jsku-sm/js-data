"""
페이지 2 — 과제 (청소년 금융이해력 분석 보고서)
"""

import streamlit as st
import pandas as pd
from pathlib import Path


def render():

    # ── 헤더 ──────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#1a1612,#3a2010);
                    border-radius:16px; padding:36px 40px; margin-bottom:28px; position:relative; overflow:hidden;">
            <div style="position:absolute; inset:0; background:repeating-linear-gradient(
                0deg, transparent, transparent 39px,
                rgba(255,255,255,0.03) 39px, rgba(255,255,255,0.03) 40px);"></div>
            <div style="position:relative;">
                <p style="color:#e8c4b0; margin:0 0 8px; font-size:0.8rem; font-weight:600;
                           letter-spacing:3px; text-transform:uppercase;">
                    데이터 분석 연구 보고서 · 2023 청소년 금융이해력 조사
                </p>
                <h1 style="color:white; margin:0 0 10px; font-size:1.75rem; line-height:1.4; font-weight:800;">
                    📊 중·고등학생의 부모 금융교육이<br>
                    <span style="color:#e8c4b0;">청소년 금융이해력</span>에 미치는 영향
                </h1>
                <p style="color:#c9a080; margin:0 0 20px; font-size:0.88rem;">
                    금융 웰빙의 매개효과를 중심으로
                </p>
                <div style="display:flex; gap:28px; flex-wrap:wrap;">
                    <div style="border-left:2px solid #b5451b; padding-left:12px;">
                        <div style="font-size:0.7rem; letter-spacing:2px; text-transform:uppercase; color:#aaa; margin-bottom:3px;">표본 수</div>
                        <div style="font-size:0.9rem; color:white; font-weight:500;">5,716명 (유효 표본)</div>
                    </div>
                    <div style="border-left:2px solid #b5451b; padding-left:12px;">
                        <div style="font-size:0.7rem; letter-spacing:2px; text-transform:uppercase; color:#aaa; margin-bottom:3px;">분석 방법</div>
                        <div style="font-size:0.9rem; color:white; font-weight:500;">다중선형회귀분석 (OLS)</div>
                    </div>
                    <div style="border-left:2px solid #b5451b; padding-left:12px;">
                        <div style="font-size:0.7rem; letter-spacing:2px; text-transform:uppercase; color:#aaa; margin-bottom:3px;">대상</div>
                        <div style="font-size:0.9rem; color:white; font-weight:500;">중·고등학생</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 탭 구성 ───────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["① 데이터 소개", "② 연구 설계", "③ 분석 방법", "④ 분석 결과", "⑤ 결론 및 시사점"]
    )

    # ══════════════════════════════════════════════════════════════
    # TAB 1 — 데이터 소개
    # ══════════════════════════════════════════════════════════════
    with tab1:
        st.markdown(
            """
            <div style="font-size:0.75rem; letter-spacing:3px; text-transform:uppercase;
                        color:#b5451b; font-weight:700; margin-bottom:8px;">Section 01</div>
            """, unsafe_allow_html=True
        )
        st.subheader("데이터 소개")

        st.markdown(
            """
            <p style="color:#333; font-size:0.95rem; line-height:1.9;">
            본 연구는
            <strong>「2023 청소년 금융이해력 및 금융생활실태 조사」</strong>
            데이터를 활용합니다. 이 데이터는 전국 중·고등학생을 대상으로
            금융 지식, 금융 행위, 부모 및 학교 금융교육 경험, 금융 웰빙 수준 등을 측정한
            대규모 설문조사입니다.
            </p>
            """,
            unsafe_allow_html=True,
        )

        # 표본 지표
        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            ("5,888", "원본 총 표본 수", "#b5451b"),
            ("5,716", "결측치 제거 후 유효 표본", "#1a1612"),
            ("172", "제거된 결측 행", "#7a6f63"),
            ("13", "금융이해력 측정 문항 수", "#1a1612"),
        ]
        for col, (val, label, color) in zip([c1, c2, c3, c4], metrics):
            with col:
                st.markdown(
                    f"""
                    <div style="background:white; border:1px solid #d4c9b8; border-top:3px solid {color};
                                border-radius:4px; padding:20px 18px; text-align:center;">
                        <div style="font-size:2rem; font-weight:800; color:{color}; line-height:1;">{val}</div>
                        <div style="font-size:0.78rem; color:#7a6f63; margin-top:8px; line-height:1.4;">{label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 변수 구성")

        var_data = {
            "변수 유형": ["종속변수", "독립변수 1", "독립변수 2", "독립변수 3", "통제변수"],
            "변수명": ["금융이해력 종합점수", "부모 금융교육 수준", "학교 금융교육 경험", "금융 웰빙", "부모학력, 성별, 학년"],
            "질문 ID": ["Q02~Q14", "Q26 (7문항)", "Q27", "Q33 (5문항)", "DQ8, DQ2, 학년"],
            "설명": [
                "금융지식 7문항 + 금융행위 6문항 합산 종합지수",
                "용돈 사용 지도, 저축 방법 안내 등 부모의 7가지 금융교육 항목 합산점수 (4점 척도)",
                "학교에서의 금융교육 수강 여부, 방식, 실생활 도움 정도",
                "경제적 여유, 금융 불안감 등 5문항 합산점수",
                "사회경제적 배경 효과를 통제하는 변수들",
            ],
        }
        st.dataframe(pd.DataFrame(var_data), use_container_width=True, hide_index=True)

        st.markdown(
            """
            <div style="background:#fff4e0; border:1px solid #e8c4b0; border-radius:8px;
                        padding:16px 20px; margin-top:16px; font-size:0.88rem; color:#3a2010; line-height:1.8;">
                세 독립변수는 각각 <strong>가정(비형식)</strong>, <strong>학교(형식)</strong>,
                <strong>심리적 상태</strong>라는 서로 다른 층위를 대표하여,
                다중회귀분석 시 각 영역의 독립적 기여도를 깔끔하게 비교할 수 있습니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════
    # TAB 2 — 연구 설계
    # ══════════════════════════════════════════════════════════════
    with tab2:
        st.markdown(
            """
            <div style="font-size:0.75rem; letter-spacing:3px; text-transform:uppercase;
                        color:#b5451b; font-weight:700; margin-bottom:8px;">Section 02</div>
            """, unsafe_allow_html=True
        )
        st.subheader("연구 설계")

        st.markdown(
            """
            <p style="color:#333; font-size:0.95rem; line-height:1.9;">
            본 연구는 청소년의 금융이해력에 영향을 미치는 교육적·심리적 요인을 규명하기 위해 설계되었습니다.
            가정과 학교라는 두 가지 금융교육 경로와, 개인 심리 상태로서의 금융 웰빙이
            금융이해력에 미치는 상대적 효과를 체계적으로 분석합니다.
            </p>
            """,
            unsafe_allow_html=True,
        )

        cards = [
            ("🎯", "연구 목적", "부모 금융교육, 학교 금융교육, 금융 웰빙이 청소년 금융이해력에 미치는 독립적 영향 검증"),
            ("📐", "연구 설계", "횡단적 설문 데이터를 활용한 다중선형회귀분석 (OLS) 기반 양적 연구"),
            ("💡", "이론적 배경", "금융사회화(Financial Socialization) 이론 — 가정·학교 환경이 금융 행동 형성에 미치는 영향"),
            ("❓", "핵심 연구 질문", "부모 금융교육이 학교 교육 및 금융 웰빙 대비 금융이해력에 더 강한 영향을 미치는가?"),
        ]

        c1, c2 = st.columns(2)
        for i, (icon, title, desc) in enumerate(cards):
            col = c1 if i % 2 == 0 else c2
            with col:
                st.markdown(
                    f"""
                    <div style="background:white; border:1px solid #d4c9b8; border-top:3px solid #b5451b;
                                border-radius:4px; padding:22px; margin-bottom:16px; min-height:130px;">
                        <div style="font-size:1.6rem; margin-bottom:10px;">{icon}</div>
                        <div style="font-weight:700; color:#1a1612; font-size:0.9rem; margin-bottom:8px;">{title}</div>
                        <div style="color:#7a6f63; font-size:0.83rem; line-height:1.7;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("#### 연구 모형")
        st.markdown(
            """
            <div style="background:#faf8f4; border:1px solid #d4c9b8; border-radius:8px;
                        padding:24px; text-align:center; font-size:0.92rem;">
                <div style="display:flex; justify-content:center; align-items:center;
                            gap:0; flex-wrap:wrap; font-size:0.9rem;">
                    <div style="display:flex; flex-direction:column; gap:10px; margin-right:16px;">
                        <div style="background:#e8c4b0; border-radius:6px; padding:10px 18px;
                                    font-weight:600; color:#3a2010;">부모 금융교육 (Q26)</div>
                        <div style="background:#e8c4b0; border-radius:6px; padding:10px 18px;
                                    font-weight:600; color:#3a2010;">학교 금융교육 (Q27)</div>
                        <div style="background:#e8c4b0; border-radius:6px; padding:10px 18px;
                                    font-weight:600; color:#3a2010;">금융 웰빙 (Q33)</div>
                    </div>
                    <div style="font-size:2rem; color:#b5451b; margin:0 16px;">→</div>
                    <div style="background:#b5451b; border-radius:6px; padding:16px 24px;
                                font-weight:700; color:white; font-size:1rem;">
                        금융이해력<br>
                        <span style="font-weight:400; font-size:0.8rem;">(지식 + 행위 종합점수)</span>
                    </div>
                </div>
                <div style="margin-top:16px; color:#7a6f63; font-size:0.82rem;">
                    통제변수: 부모학력(DQ8), 성별(DQ2), 학년
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════
    # TAB 3 — 분석 방법
    # ══════════════════════════════════════════════════════════════
    with tab3:
        st.markdown(
            """
            <div style="font-size:0.75rem; letter-spacing:3px; text-transform:uppercase;
                        color:#b5451b; font-weight:700; margin-bottom:8px;">Section 03</div>
            """, unsafe_allow_html=True
        )
        st.subheader("분석 방법")

        st.markdown(
            """
            <p style="color:#333; font-size:0.95rem; line-height:1.9; margin-bottom:24px;">
            데이터 탐색부터 회귀분석까지 총 4단계의 체계적인 분석 절차를 거쳤습니다.
            Python 기반의 통계 라이브러리(pandas, statsmodels, seaborn)를 활용하였습니다.
            </p>
            """,
            unsafe_allow_html=True,
        )

        steps = [
            (
                "1", "탐색적 데이터 분석 (EDA)",
                "종속변수(Q02~Q14)의 기초통계량 및 상자 그림으로 분포를 파악하고, "
                "독립변수(Q26, Q27, Q33)의 히스토그램으로 왜도(skewness)를 확인합니다. "
                "결측치를 탐색하여 독립변수 결측 172개 행을 목록제거(listwise deletion) 방식으로 처리합니다.",
            ),
            (
                "2", "변수 변환 및 분석용 데이터 구성",
                "학교 금융교육 경험(Q27)을 더미 변수(Q27_2.0)로 변환하여 다중공선성을 방지합니다(drop_first=True). "
                "Q02~Q08(금융지식)과 Q09~Q14(금융행위)를 합산하여 종합 금융이해력 점수를 생성합니다.",
            ),
            (
                "3", "다중공선성 검증 (VIF)",
                "분산팽창계수(VIF; Variance Inflation Factor)를 계산하여 독립변수 간 다중공선성을 점검합니다. "
                "VIF < 10이면 문제 없음으로 판단합니다. "
                "분석 결과 모든 독립변수의 VIF = 1.00으로 나타나 다중공선성 문제가 없음을 확인합니다.",
            ),
            (
                "4", "다중선형회귀분석 (OLS)",
                "statsmodels의 OLS(Ordinary Least Squares) 모델로 독립변수들이 금융이해력 종합점수에 미치는 영향을 추정합니다. "
                "회귀계수, p-값, 95% 신뢰구간, R², F-통계량을 통해 결과를 해석합니다.",
            ),
        ]

        for num, title, desc in steps:
            st.markdown(
                f"""
                <div style="display:flex; gap:16px; align-items:flex-start; margin-bottom:20px;">
                    <div style="background:#b5451b; color:white; border-radius:50%; width:32px; height:32px;
                                display:flex; align-items:center; justify-content:center;
                                font-weight:700; font-size:0.9rem; flex-shrink:0; margin-top:2px;">{num}</div>
                    <div style="background:white; border:1px solid #d4c9b8; border-radius:4px; padding:18px 20px; flex:1;">
                        <div style="font-weight:700; color:#1a1612; margin-bottom:8px; font-size:0.95rem;">{title}</div>
                        <div style="color:#7a6f63; font-size:0.85rem; line-height:1.8;">{desc}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()
        st.markdown("#### 📊 시각화 분석 결과")
        
        # 히스토그램
        st.markdown("**• 히스토그램 — 독립변수 분포 및 왜도(Skewness)**")
        try:
            histogram_path = Path(__file__).parent.parent / "images" / "히스토그램.png"
            st.image(str(histogram_path), use_column_width=True)
        except:
            st.info("히스토그램 이미지를 찾을 수 없습니다.")
        
        # 세로상자그림
        st.markdown("**• 세로상자그림(Box Plot) — 종속변수(금융이해력) 분포**")
        try:
            boxplot_path = Path(__file__).parent.parent / "images" / "세로상자그림.png"
            st.image(str(boxplot_path), use_column_width=True)
        except:
            st.info("세로상자그림 이미지를 찾을 수 없습니다.")

        st.markdown("#### 분포 주요 발견")

        findings = [
            ("부모 금융교육 (Q26)", "낮은 점수대 집중 — 우편 왜도(right-skewed) 분포. 부모 금융교육 참여가 전반적으로 낮거나 특정 항목에 집중됨을 시사."),
            ("학교 금융교육 (Q27)", "마찬가지로 우편 왜도 분포. 학교 금융교육의 보편성이 낮음을 시사하며, 교육 경험 유무에 편차 큼."),
            ("금융 웰빙 (Q33)", "상대적으로 다양하게 분포. 학생들의 금융 불안감 수준이 개인마다 상이하여 분산이 큼."),
        ]

        for var, finding in findings:
            st.markdown(
                f"""
                <div style="background:#faf8f4; border-left:3px solid #b5451b;
                            padding:12px 18px; margin-bottom:10px; border-radius:0 4px 4px 0;">
                    <strong style="color:#1a1612;">{var}</strong><br>
                    <span style="color:#7a6f63; font-size:0.85rem;">{finding}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════
    # TAB 4 — 분석 결과
    # ══════════════════════════════════════════════════════════════
    with tab4:
        st.markdown(
            """
            <div style="font-size:0.75rem; letter-spacing:3px; text-transform:uppercase;
                        color:#b5451b; font-weight:700; margin-bottom:8px;">Section 04</div>
            """, unsafe_allow_html=True
        )
        st.subheader("분석 결과")

        # VIF
        st.markdown("#### 다중공선성 검증 (VIF)")
        vif_data = {
            "변수": ["Q26", "Q33", "Q27_2.0"],
            "설명": ["부모 금융교육 수준", "금융 웰빙", "학교 금융교육 경험 (더미)"],
            "VIF 값": [1.00, 1.00, 1.00],
            "판정": ["✅ 문제없음", "✅ 문제없음", "✅ 문제없음"],
        }
        st.dataframe(pd.DataFrame(vif_data), use_container_width=True, hide_index=True)
        st.markdown(
            """
            <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:6px;
                        padding:12px 18px; font-size:0.85rem; color:#166534; margin-bottom:24px;">
                ✅ 모든 VIF 값이 1.00으로, 독립변수 간 다중공선성 문제가 전혀 없어
                회귀계수 추정의 신뢰성이 확보됩니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # 상관관계 히트맵
        st.markdown("#### 상관관계 분석 (Correlation Heatmap)")
        st.markdown("**변수 간 상관관계 분석 — 다중공선성 사전 점검**")
        try:
            heatmap_path = Path(__file__).parent.parent / "images" / "상관관계 히트맵.png"
            st.image(str(heatmap_path), use_column_width=True)
        except:
            st.info("상관관계 히트맵 이미지를 찾을 수 없습니다.")

        st.divider()

        # 모델 적합도
        st.markdown("#### 회귀분석 모델 적합도")
        st.markdown(
            """
            <div style="background:#faf8f4; border:1px solid #d4c9b8; border-radius:6px;
                        padding:6px 18px 6px; margin-bottom:10px; font-size:0.8rem; color:#7a6f63;">
                OLS Regression — 금융이해력 종합점수
            </div>
            """,
            unsafe_allow_html=True,
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("R² (설명력)", "0.009", "0.9%")
        m2.metric("Adj. R²", "0.008")
        m3.metric("F-statistic", "16.97")
        m4.metric("Prob (F-statistic)", "2.26e-11 ***")

        st.markdown(
            """
            <div style="background:#fff4e0; border:1px solid #e8c4b0; border-radius:6px;
                        padding:14px 18px; font-size:0.87rem; color:#3a2010; line-height:1.8; margin-bottom:24px;">
                모델의 F-통계량 p-값이 0.001 미만으로 <strong>전체 모델은 통계적으로 유의미</strong>합니다.
                다만 R²=0.009는 현재 독립변수들만으로 금융이해력 변산의 약 0.9%만 설명함을 의미하며,
                추가 변수 투입이 필요함을 시사합니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # 회귀계수 결과
        st.markdown("#### 개별 독립변수 회귀계수 결과")

        results = [
            {
                "sig": True, "var": "부모 금융교육 수준 (Q26)",
                "beta": "+0.3343", "p": "0.000 (***)",
                "ci": "[0.228, 0.441]",
                "interp": "부모의 금융교육 수준이 1점 증가할수록 청소년의 금융이해력 종합점수가 평균 0.334점 유의미하게 증가",
            },
            {
                "sig": True, "var": "학교 금융교육 경험 (Q27_2.0)",
                "beta": "+0.3135", "p": "0.001 (**)",
                "ci": "신뢰구간 포함",
                "interp": "학교 금융교육 경험이 있는 학생이 없는 학생보다 금융이해력 종합점수가 평균 0.314점 더 높음",
            },
            {
                "sig": False, "var": "금융 웰빙 (Q33)",
                "beta": "+0.0734", "p": "0.226 (n.s.)",
                "ci": "—",
                "interp": "현재 모델에서 금융 웰빙은 금융이해력에 직접적·통계적으로 유의미한 영향을 보이지 않음 → 매개효과 분석 필요",
            },
        ]

        for r in results:
            badge_color = "#b5451b" if r["sig"] else "#7a6f63"
            badge_text = "유의미 ✓" if r["sig"] else "비유의미 ✗"
            bg_color = "white" if r["sig"] else "#faf8f4"

            st.markdown(
                f"""
                <div style="background:{bg_color}; border:1px solid #d4c9b8;
                            border-left:4px solid {badge_color};
                            border-radius:0 6px 6px 0; padding:20px 22px; margin-bottom:14px;">
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
                        <span style="background:{badge_color}; color:white; padding:3px 12px;
                                     border-radius:99px; font-size:0.75rem; font-weight:700;">{badge_text}</span>
                        <strong style="color:#1a1612; font-size:0.95rem;">{r["var"]}</strong>
                    </div>
                    <div style="display:flex; gap:24px; flex-wrap:wrap; margin-bottom:12px;">
                        <div>
                            <div style="font-size:0.7rem; color:#7a6f63; margin-bottom:2px;">회귀계수 (β)</div>
                            <div style="font-size:1.3rem; font-weight:800; color:{badge_color};">{r["beta"]}</div>
                        </div>
                        <div>
                            <div style="font-size:0.7rem; color:#7a6f63; margin-bottom:2px;">p-값</div>
                            <div style="font-size:1rem; font-weight:600; color:#1a1612;">{r["p"]}</div>
                        </div>
                        <div>
                            <div style="font-size:0.7rem; color:#7a6f63; margin-bottom:2px;">95% 신뢰구간</div>
                            <div style="font-size:1rem; font-weight:600; color:#1a1612;">{r["ci"]}</div>
                        </div>
                    </div>
                    <div style="color:#475569; font-size:0.85rem; line-height:1.7; border-top:1px solid #e8e0d8; padding-top:10px;">
                        💬 {r["interp"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        # 결과 요약 비교표
        st.markdown("#### 결과 요약 비교")
        summary_data = {
            "독립변수": ["부모 금융교육 (Q26)", "학교 금융교육 (Q27)", "금융 웰빙 (Q33)"],
            "회귀계수": [0.3343, 0.3135, 0.0734],
            "p-값": ["0.000", "0.001", "0.226"],
            "유의성": ["*** 매우 유의", "** 유의", "n.s. 비유의"],
            "효과 방향": ["📈 긍정적", "📈 긍정적", "— 불명확"],
        }
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════════════════════════
    # TAB 5 — 결론 및 시사점
    # ══════════════════════════════════════════════════════════════
    with tab5:
        st.markdown(
            """
            <div style="font-size:0.75rem; letter-spacing:3px; text-transform:uppercase;
                        color:#b5451b; font-weight:700; margin-bottom:8px;">Section 05</div>
            """, unsafe_allow_html=True
        )
        st.subheader("결론 및 시사점")

        st.markdown(
            """
            <p style="color:#333; font-size:0.95rem; line-height:1.9;">
            본 연구의 다중선형회귀분석 결과, <strong>청소년의 금융이해력은 부모 금융교육 수준과
            학교 금융교육 경험에 의해 통계적으로 유의미한 긍정적 영향을 받는 것</strong>으로 나타났습니다.
            반면 금융 웰빙은 직접적인 영향이 확인되지 않아, 매개 경로에 대한 심층 분석이 필요합니다.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 📌 주요 발견")
        findings = [
            "부모 금융교육(β=0.334)과 학교 금융교육(β=0.314) 모두 금융이해력을 유의미하게 향상시킴",
            "두 교육 변수의 효과 크기가 유사하여, 가정과 학교 교육 모두 중요함을 시사",
            "독립변수 간 다중공선성 없음 → 각 교육 채널의 독립적 효과 신뢰 가능",
            "금융 웰빙은 직접 효과보다 간접(매개) 경로로 작용할 가능성",
        ]
        for f in findings:
            st.markdown(
                f"""
                <div style="display:flex; gap:10px; align-items:flex-start; margin-bottom:8px;">
                    <span style="color:#b5451b; font-size:1rem; flex-shrink:0; margin-top:1px;">◆</span>
                    <span style="color:#333; font-size:0.88rem; line-height:1.7;">{f}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        st.markdown("#### ⚠️ 한계 및 제언")
        limits = [
            "R²=0.9%로 설명력 낮음 → 학년, 성별, 부모학력 등 통제변수 포함 필요",
            "금융 웰빙의 매개효과는 OLS로 검증 불가 → 구조방정식 모델링(SEM) 필요",
            "횡단 자료 한계 → 인과관계보다 상관관계로 해석 요망",
            "금융교육 내용·질적 차이를 반영하는 세분화 분석 권장",
        ]
        for lim in limits:
            st.markdown(
                f"""
                <div style="display:flex; gap:10px; align-items:flex-start; margin-bottom:8px;">
                    <span style="color:#7a6f63; font-size:1rem; flex-shrink:0; margin-top:1px;">•</span>
                    <span style="color:#475569; font-size:0.87rem; line-height:1.7;">{lim}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        # 정책적 시사점
        st.markdown("#### 정책적 시사점")

        policies = [
            ("🏫", "#b5451b", "학교 교육 정책",
             "학교 금융교육이 금융이해력을 유의미하게 향상시키므로, 교과 내 금융교육 의무화 및 질적 강화 정책이 효과적일 수 있습니다."),
            ("👨‍👩‍👧", "#3a2010", "가정 교육 지원",
             "부모 금융교육이 가장 강한 효과를 보임에 따라, 부모 대상 금융교육 프로그램 지원 및 가정 내 금융 대화 촉진 캠페인이 필요합니다."),
            ("🧠", "#7a6f63", "금융 웰빙 연구",
             "금융 웰빙의 매개 경로 규명을 위한 후속 연구가 요구되며, 청소년의 금융 불안 해소 프로그램 개발도 고려할 수 있습니다."),
        ]

        p1, p2, p3 = st.columns(3)
        for col, (icon, color, title, desc) in zip([p1, p2, p3], policies):
            with col:
                st.markdown(
                    f"""
                    <div style="background:white; border:1px solid #d4c9b8; border-top:3px solid {color};
                                border-radius:4px; padding:22px 18px; height:200px;">
                        <div style="font-size:1.8rem; margin-bottom:10px;">{icon}</div>
                        <div style="font-weight:700; color:#1a1612; margin-bottom:10px; font-size:0.9rem;">{title}</div>
                        <div style="color:#7a6f63; font-size:0.8rem; line-height:1.7;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # 다음 단계
        st.markdown(
            """
            <div style="background:#faf8f4; border:1px solid #d4c9b8; border-radius:6px;
                        padding:20px 24px; margin-top:20px; font-size:0.87rem; color:#3a2010; line-height:1.9;">
                <strong>📌 다음 단계 제언</strong><br>
                통제변수(학년, 성별, 부모학력)를 포함한 확장 회귀모델 분석과 함께,
                금융 웰빙의 <strong>매개효과 검증(Structural Equation Modeling)</strong>을 진행하여
                부모 금융교육 → 금융 웰빙 → 금융이해력의 경로를 규명하는 것이 본 연구의 핵심 과제인
                "매개효과 분석"을 완성하는 데 필수적입니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 푸터
        st.markdown(
            """
            <div style="background:#1a1612; border-radius:10px; padding:20px 24px;
                        margin-top:24px; text-align:center;">
                <div style="color:#7a6f63; font-size:0.78rem; margin-bottom:6px;">
                    2023 청소년 금융이해력 및 금융생활실태 조사 데이터 기반 분석 보고서
                </div>
                <div style="color:#e8c4b0; font-weight:600; font-size:0.9rem;">
                    AI융합교육전공 · 2542100 구정숙
                </div>
                <div style="color:#7a6f63; font-size:0.78rem; margin-top:6px;">
                    분석 도구: Python · pandas · statsmodels · seaborn
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
