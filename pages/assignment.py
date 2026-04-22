"""
페이지 2 — 과제 (청소년 금융이해력 분석 보고서)
"""

import streamlit as st
import pandas as pd

_BOXPLOT_B64 = "생략" # 실제 코드에는 긴 문자열이 포함되어 있습니다.
_HIST_B64 = "생략" # 실제 코드에는 긴 문자열이 포함되어 있습니다.
_CORR_B64 = "생략" # 실제 코드에는 긴 문자열이 포함되어 있습니다.

def _img_html(b64_str, alt_text=""):
    return f'<img src="data:image/png;base64,{b64_str}" alt="{alt_text}" style="width:100%; border-radius:8px; border:1px solid #eee; margin-bottom:10px;">'

def render():
    st.title("청소년 금융이해력 분석 보고서")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["① 데이터 소개", "② 연구 설계", "③ 분석 방법", "④ 분석 결과", "⑤ 결론 및 시사점"]
    )

    # ══════════════════════════════════════════════════════════════
    # TAB 1 — 데이터 소개
    # ══════════════════════════════════════════════════════════════
    with tab1:
        st.markdown(
            '<div style="font-size:0.75rem;letter-spacing:3px;text-transform:uppercase;'
            'color:#b5451b;font-weight:700;margin-bottom:8px;">Section 01</div>',
            unsafe_allow_html=True,
        )
        st.subheader("데이터 소개")
        st.markdown(
            '<p style="color:#333;font-size:0.95rem;line-height:1.9;">'
            '본 분석은 청소년의 금융이해력에 영향을 미치는 요인을 파악하기 위해 수행되었습니다. '
            '부모와 학교의 금융교육 경험, 그리고 개인의 금융 웰빙 상태가 실제 금융이해력 점수와 어떤 상관관계를 갖는지 분석합니다.</p>',
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════
    # TAB 2 — 연구 설계
    # ══════════════════════════════════════════════════════════════
    with tab2:
        st.markdown(
            '<div style="font-size:0.75rem;letter-spacing:3px;text-transform:uppercase;'
            'color:#b5451b;font-weight:700;margin-bottom:8px;">Section 02</div>',
            unsafe_allow_html=True,
        )
        st.subheader("연구 설계")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("독립변수: 부모 금융교육(Q26), 학교 금융교육(Q27), 금융 웰빙(Q33)")
        with col2:
            st.success("종속변수: 금융이해력 점수 (Q02~Q14 합산)")

    # ══════════════════════════════════════════════════════════════
    # TAB 3 — 분석 방법
    # ══════════════════════════════════════════════════════════════
    with tab3:
        st.markdown(
            '<div style="font-size:0.75rem;letter-spacing:3px;text-transform:uppercase;'
            'color:#b5451b;font-weight:700;margin-bottom:8px;">Section 03</div>',
            unsafe_allow_html=True,
        )
        st.subheader("분석 방법")
        st.markdown(
            '<p style="color:#333;font-size:0.95rem;line-height:1.9;margin-bottom:24px;">'
            '데이터 탐색부터 회귀분석까지 총 4단계의 체계적인 분석 절차를 거쳤습니다. '
            '구글코랩-Python 기반의 통계 라이브러리(pandas, statsmodels, seaborn)를 활용하였습니다.</p>',
            unsafe_allow_html=True,
        )
        for num, title, desc in [
            ("1", "탐색적 데이터 분석 (EDA)",
             "종속변수(Q02~Q14)의 기초통계량 및 상자 그림으로 분포를 파악하고, 독립변수(Q26, Q27, Q33)의 히스토그램으로 왜도를 확인합니다."),
            ("2", "변수 변환 및 분석용 데이터 구성",
             "학교 금융교육 경험(Q27)을 더미 변수로 변환하여 다중공선성을 방지하고 분석용 데이터셋을 구축합니다."),
            ("3", "상관관계 분석",
             "변수 간의 선형적 관계를 히트맵으로 시각화하여 변수 간의 연관성을 파악합니다."),
            ("4", "다중선형회귀분석",
             "OLS 방식을 사용하여 독립변수들이 금융이해력에 미치는 영향력과 통계적 유의성을 검증합니다."),
        ]:
            st.markdown(
                f'<div style="display:flex;gap:15px;margin-bottom:15px;">'
                f'<div style="background:#b5451b;color:white;width:28px;height:28px;border-radius:50%;'
                f'display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0;font-size:0.85rem;">{num}</div>'
                f'<div style="background:white;border:1px solid #d4c9b8;border-radius:4px;padding:18px 20px;flex:1;">'
                f'<div style="font-weight:700;color:#1a1612;margin-bottom:8px;font-size:0.95rem;">{title}</div>'
                f'<div style="color:#7a6f63;font-size:0.85rem;line-height:1.8;">{desc}</div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════
    # TAB 4 — 분석 결과
    # ══════════════════════════════════════════════════════════════
    with tab4:
        st.markdown(
            '<div style="font-size:0.75rem;letter-spacing:3px;text-transform:uppercase;'
            'color:#b5451b;font-weight:700;margin-bottom:8px;">Section 04</div>',
            unsafe_allow_html=True,
        )
        st.subheader("분석 결과")

        # --- 분석 방법에서 이동된 시각화 섹션 시작 ---
        # 그림 1: 상자 그림
        st.markdown("---")
        st.markdown("#### 종속변수 문항별 점수 분포")
        st.markdown(_img_html(_BOXPLOT_B64, "종속변수 상자 그림"), unsafe_allow_html=True)
        st.markdown(
            '<div style="background:#faf8f4;border:1px solid #d4c9b8;border-radius:6px;'
            'padding:12px 18px;font-size:0.83rem;color:#7a6f63;margin-top:4px;">'
            '▲ <strong>그림 1.</strong> 금융이해력 각 문항(Q02~Q14) 점수 분포 (상자 그림). '
            'Q02~Q08(금융지식)은 낮은 점수대에 집중되며, Q11~Q14(금융행위)는 상대적으로 분포 범위가 넓습니다. 용돈 관리나 저축 같은 실제 행동은 어떤 학생은 잘 하고, 어떤 학생은 전혀 안 한다는 것을 보여줍니다.</div>',
            unsafe_allow_html=True,
        )

        # 분포 주요 발견
        st.markdown("#### 분포 주요 발견")
        for var, finding in [
            ("부모 금융교육 (Q26)", "낮은 점수대 집중 — 우편 왜도(right-skewed) 분포. 부모 금융교육 참여가 전반적으로 낮거나 특정 항목에 집중됨을 시사."),
            ("학교 금융교육 (Q27)", "마찬가지로 우편 왜도 분포. 학교 금융교육의 보편성이 낮음을 시사하며, 교육 경험 유무에 편차 큼."),
            ("금융 웰빙 (Q33)", "상대적으로 다양하게 분포. 학생들의 금융 불안감 수준이 개인마다 상이하여 분산이 큼."),
        ]:
            st.markdown(
                f'<div style="background:#faf8f4;border-left:3px solid #b5451b;'
                f'padding:12px 18px;margin-bottom:10px;border-radius:0 4px 4px 0;">'
                f'<strong style="color:#1a1612;">{var}</strong><br>'
                f'<span style="color:#7a6f63;font-size:0.85rem;">{finding}</span></div>',
                unsafe_allow_html=True,
            )

        # 그림 2: 히스토그램
        st.markdown("---")
        st.markdown("#### 독립변수 점수 분포 (히스토그램)")
        st.markdown(_img_html(_HIST_B64, "독립변수 히스토그램"), unsafe_allow_html=True)
        st.markdown(
            '<div style="background:#faf8f4;border:1px solid #d4c9b8;border-radius:6px;'
            'padding:12px 18px;font-size:0.83rem;color:#7a6f63;margin-top:4px;">'
            '▲ <strong>그림 2.</strong> 독립변수 히스토그램. '
            '부모 금융교육(Q26)과 학교 금융교육(Q27)은 낮은 점수에 집중된 우편 왜도(right-skewed) 분포를 보임. '
            '금융 웰빙(Q33)은 봉우리가 두 개인 이봉(bimodal) 분포 양상을 띰.</div>',
            unsafe_allow_html=True,
        )
        # --- 분석 방법에서 이동된 시각화 섹션 끝 ---

        st.divider()
        st.markdown("#### 다중공선성 검증 (VIF)")
        st.dataframe(
            pd.DataFrame({
                "변수": ["Q26", "Q33", "Q27_2.0"],
                "설명": ["부모 금융교육 수준", "금융 웰빙", "학교 금융교육 경험 (더미)"],
                "VIF 값": [1.00, 1.00, 1.00],
                "판정": ["✅ 문제없음", "✅ 문제없음", "✅ 문제없음"],
            }),
            use_container_width=True, hide_index=True,
        )

        st.markdown("#### 변수 간 상관 행렬")
        st.markdown(_img_html(_CORR_B64, "상관 행렬 히트맵"), unsafe_allow_html=True)

        st.divider()
        st.markdown("#### 회귀분석 결과 요약")
        st.dataframe(
            pd.DataFrame({
                "독립변수": ["부모 금융교육 (Q26)", "학교 금융교육 (Q27)", "금융 웰빙 (Q33)"],
                "회귀계수": [0.3343, 0.3135, 0.0734],
                "p-값": ["0.000", "0.001", "0.226"],
                "유의성": ["*** 매우 유의", "** 유의", "n.s. 비유의"],
            }),
            use_container_width=True, hide_index=True,
        )

    # ══════════════════════════════════════════════════════════════
    # TAB 5 — 결론 및 시사점
    # ══════════════════════════════════════════════════════════════
    with tab5:
        st.markdown(
            '<div style="font-size:0.75rem;letter-spacing:3px;text-transform:uppercase;'
            'color:#b5451b;font-weight:700;margin-bottom:8px;">Section 05</div>',
            unsafe_allow_html=True,
        )
        st.subheader("결론 및 시사점")
        st.markdown(
            '<p style="color:#333;font-size:0.95rem;line-height:1.9;">'
            '분석 결과, 부모와 학교의 금융교육은 청소년의 금융이해력에 매우 유의미한 정(+)의 영향을 미치는 것으로 나타났습니다. '
            '반면 금융 웰빙은 통계적으로 유의미한 영향을 주지 못했는데, 이는 매개효과 등을 고려한 추가 분석이 필요함을 시사합니다.</p>',
            unsafe_allow_html=True,
        )
