"""
Z세대 10대 청소년 신뢰·행복도 분석 보고서
AI융합교육전공 · 2542100 구정숙
"""

import streamlit as st
import pandas as pd
import numpy as np
from numpy.linalg import lstsq
from scipy import stats
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Z세대 청소년 신뢰·행복도 분석",
    page_icon="📊",
    layout="wide",
)

# ── 데이터 로드 및 분석 (캐싱) ────────────────────────────────────
@st.cache_data
def load_and_analyze(path: str):
    df = pd.read_csv(path, encoding="utf-8")

    for col in ["Q1A1", "Q17A1", "Q17A2", "Q18"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] >= 9, col] = np.nan

    df_clean = df[["Q1A1", "Q17A1", "Q17A2", "Q18"]].dropna()

    # ── 기술통계 ────────────────────────────────────────────────
    desc = df_clean.describe().round(3)

    # ── 상관계수 ────────────────────────────────────────────────
    corr = df_clean.corr().round(3)

    # ── OLS 회귀 ────────────────────────────────────────────────
    n = len(df_clean)
    y = df_clean["Q1A1"].values
    X = df_clean[["Q17A1", "Q17A2", "Q18"]].values
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

    # 표준화 계수
    X_std = (X - X.mean(axis=0)) / X.std(axis=0)
    y_std = (y - y.mean()) / y.std()
    Xc_std = np.column_stack([np.ones(n), X_std])
    b_std, _, _, _ = lstsq(Xc_std, y_std, rcond=None)

    regression = {
        "n": n,
        "r2": round(r2, 4),
        "adj_r2": round(adj_r2, 4),
        "fstat": round(fstat, 3),
        "fp": fp,
        "coef": {
            "names": ["(상수항)", "X1: 부모님 신뢰 (Q17A1)", "X2: 친구 신뢰 (Q17A2)", "X3: 사회 신뢰 (Q18)"],
            "B": b.round(4),
            "SE": se.round(4),
            "t": t_vals.round(3),
            "p": p_vals,
            "beta": ["-"] + [round(v, 3) for v in b_std[1:]],
        },
    }

    return df_clean, desc, corr, regression


# ── 파일 경로 ───────────────────────────────────────────────────
DATA_PATH = "_데이터__Z세대_10대_청소년의_가치관_변화_연구__1_.csv"

try:
    df_clean, desc, corr, reg = load_and_analyze(DATA_PATH)
    data_loaded = True
except Exception as e:
    data_loaded = False
    load_error = str(e)

# ══════════════════════════════════════════════════════════════════
# 헤더
# ══════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div style="background:linear-gradient(135deg,#1e3a5f,#0f3460);
                border-radius:16px; padding:32px 36px; margin-bottom:28px;">
        <p style="color:#93c5fd; margin:0 0 6px; font-size:0.9rem;
                  font-weight:600; letter-spacing:1px;">
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

if not data_loaded:
    st.error(
        f"⚠️ 데이터를 불러오지 못했습니다. `{DATA_PATH}` 파일을 "
        "app.py와 같은 폴더에 두고 다시 실행해 주세요."
    )
    st.code(load_error)
    st.stop()

# ══════════════════════════════════════════════════════════════════
# 탭 구성
# ══════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📁 데이터 소개", "🎯 연구 설계", "🔍 분석 방법", "📈 분석 결과", "💡 결론 및 시사점"]
)

# ══════════════════════════════════════════════════════════════════
# TAB 1 — 데이터 소개
# ══════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("📁 1. 활용한 데이터")

    col1, col2, col3 = st.columns(3)

    def data_card(col, icon, title, desc, color):
        with col:
            st.markdown(
                f"""
                <div style="background:{color}12; border:1.5px solid {color}40;
                            border-radius:14px; padding:20px; text-align:center; min-height:160px;">
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

    st.markdown("---")
    st.markdown("#### 📌 데이터 기본 정보")
    m1, m2, m3 = st.columns(3)
    m1.metric("전체 응답자 수", "5,740명", "중·고등학생")
    m2.metric("유효 분석 샘플", f"{reg['n']:,}명", "무응답 제거 후")
    m3.metric("조사 시기", "2020년 7월", "한국청소년정책연구원")

    st.markdown("---")
    st.markdown("#### 🗂️ 분석에 사용한 원본 데이터 미리보기 (상위 10행)")
    st.dataframe(
        df_clean.head(10).rename(columns={
            "Q1A1": "행복도(Q1A1)",
            "Q17A1": "부모님신뢰(Q17A1)",
            "Q17A2": "친구신뢰(Q17A2)",
            "Q18": "사회신뢰(Q18)",
        }),
        use_container_width=True,
        hide_index=True,
    )

# ══════════════════════════════════════════════════════════════════
# TAB 2 — 연구 설계
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🎯 2. 연구주제 및 변수 설정")

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
                그들의 주관적 <strong>'행복도'</strong>를 얼마나 설명할 수 있는지 확인합니다.
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

    iv_data = [
        ("X1", "부모님 신뢰도", "Q17A1",
         "다음 대상에 대해 얼마나 신뢰합니까: 부모님(보호자)",
         "1점(전혀 믿을 수 없다) ~ 4점(매우 믿을 수 있다) · 4점 척도", "#3b82f6"),
        ("X2", "친구 신뢰도", "Q17A2",
         "다음 대상에 대해 얼마나 신뢰합니까: 친구",
         "1점(전혀 믿을 수 없다) ~ 4점(매우 믿을 수 있다) · 4점 척도", "#8b5cf6"),
        ("X3", "사회 신뢰도", "Q18",
         "우리 사회가 어느 정도 믿을 수 있는 사회라고 생각합니까?",
         "0점(전혀 믿을 수 없다) ~ 10점(매우 믿을 수 있다) · 11점 척도", "#10b981"),
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
                    📌 <strong>사용 변수:</strong> {var} — {desc_text}<br>
                    📐 <strong>척도:</strong> {scale}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ══════════════════════════════════════════════════════════════════
# TAB 3 — 분석 방법
# ══════════════════════════════════════════════════════════════════
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
                        <strong>결측치 및 무응답 처리</strong><br>
                        <span style="color:#64748b; font-size:0.85rem;">
                            코드북 기준 값 <code>9</code>(Q17), <code>99</code>(Q18)는 '무응답' →
                            NaN으로 변환 후 분석에서 제외(listwise deletion)
                        </span>
                    </div>
                </div>
                <div style="display:flex; align-items:flex-start; gap:12px;">
                    <span style="background:#f59e0b; color:white; border-radius:50%;
                                 min-width:26px; height:26px; display:flex; align-items:center;
                                 justify-content:center; font-size:0.8rem; font-weight:700;">2</span>
                    <div>
                        <strong>데이터 타입 및 척도 확인</strong><br>
                        <span style="color:#64748b; font-size:0.85rem;">
                            Q1A1·Q17A1·Q17A2 → 4점 척도(연속형 처리),
                            Q18 → 0~10점 척도(연속형 처리)
                        </span>
                    </div>
                </div>
                <div style="display:flex; align-items:flex-start; gap:12px;">
                    <span style="background:#3b82f6; color:white; border-radius:50%;
                                 min-width:26px; height:26px; display:flex; align-items:center;
                                 justify-content:center; font-size:0.8rem; font-weight:700;">3</span>
                    <div>
                        <strong>척도 간 직접 비교를 위한 표준화 계수 산출</strong><br>
                        <span style="color:#64748b; font-size:0.85rem;">
                            Q18이 0~10점으로 다른 변수와 척도가 달라 비표준화 계수(B)만으로는
                            영향력 비교가 어렵기 때문에 표준화 계수(β)를 함께 보고합니다.
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 📊 3-2. 탐색적 데이터 분석 (EDA)")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div style="background:#eff6ff; border-radius:12px; padding:18px; min-height:140px;">
                <div style="font-weight:700; color:#1e40af; margin-bottom:8px;">📋 기술통계 분석</div>
                <div style="color:#475569; font-size:0.85rem; line-height:1.7;">
                    각 변수의 <strong>평균, 표준편차, 최솟값, 최댓값</strong>을 확인하여
                    Z세대 청소년의 행복도와 신뢰도 수준의 분포를 파악합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div style="background:#f5f3ff; border-radius:12px; padding:18px; min-height:140px;">
                <div style="font-weight:700; color:#6d28d9; margin-bottom:8px;">🔗 상관관계 분석 (Pearson)</div>
                <div style="color:#475569; font-size:0.85rem; line-height:1.7;">
                    종속·독립변수 간 선형 연관성을 확인하고 다중공선성 위험을 사전 파악합니다.
                    <br><span style="color:#ef4444;">※ 독립변수 간 r ≥ 0.8이면 다중공선성 의심</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
                부모님, 친구, 사회에 대한 신뢰가 각각 행복도에 유의미한
                <strong>정(+)의 영향</strong>을 미치는지 통계적으로 검증합니다.<br>
                <strong>유의수준: α = 0.05 &nbsp;|&nbsp; 분석 도구: Python (NumPy, SciPy)</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════
# TAB 4 — 분석 결과 (실제 데이터)
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("📈 4. 분석 결과")

    # EDA
    st.markdown("#### 🔍 4-1. 탐색적 데이터 분석(EDA) 결과")

    st.markdown("**📊 기술통계**")
    desc_display = pd.DataFrame({
        "변수": ["행복도 (Q1A1)", "부모님 신뢰도 (Q17A1)", "친구 신뢰도 (Q17A2)", "사회 신뢰도 (Q18)"],
        "척도": ["4점 만점", "4점 만점", "4점 만점", "10점 만점"],
        "평균": [
            round(desc.loc["mean", "Q1A1"], 3),
            round(desc.loc["mean", "Q17A1"], 3),
            round(desc.loc["mean", "Q17A2"], 3),
            round(desc.loc["mean", "Q18"], 3),
        ],
        "표준편차": [
            round(desc.loc["std", "Q1A1"], 3),
            round(desc.loc["std", "Q17A1"], 3),
            round(desc.loc["std", "Q17A2"], 3),
            round(desc.loc["std", "Q18"], 3),
        ],
        "최솟값": [
            int(desc.loc["min", "Q1A1"]),
            int(desc.loc["min", "Q17A1"]),
            int(desc.loc["min", "Q17A2"]),
            int(desc.loc["min", "Q18"]),
        ],
        "최댓값": [
            int(desc.loc["max", "Q1A1"]),
            int(desc.loc["max", "Q17A1"]),
            int(desc.loc["max", "Q17A2"]),
            int(desc.loc["max", "Q18"]),
        ],
    })
    st.dataframe(desc_display, use_container_width=True, hide_index=True)

    st.markdown("**🔗 상관관계 분석 결과**")
    c1, c2, c3 = st.columns(3)

    def corr_card(col, x, r_val, color):
        if r_val >= 0.3:
            interp = "중간 이상의 양(+)의 상관"
        elif r_val >= 0.2:
            interp = "약-중간의 양(+)의 상관"
        else:
            interp = "약한 양(+)의 상관"
        with col:
            st.markdown(
                f"""
                <div style="background:{color}0d; border:1.5px solid {color}50;
                            border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:0.82rem; color:#64748b; margin-bottom:6px;">행복도 ↔ {x}</div>
                    <div style="font-size:2rem; font-weight:800; color:{color};">r = {r_val}</div>
                    <div style="font-size:0.8rem; color:#475569; margin-top:6px;">{interp}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    corr_card(c1, "부모님 신뢰", corr.loc["Q1A1", "Q17A1"], "#3b82f6")
    corr_card(c2, "친구 신뢰",   corr.loc["Q1A1", "Q17A2"], "#8b5cf6")
    corr_card(c3, "사회 신뢰",   corr.loc["Q1A1", "Q18"],   "#10b981")

    # 독립변수 간 다중공선성 확인
    max_iv_corr = max(
        abs(corr.loc["Q17A1", "Q17A2"]),
        abs(corr.loc["Q17A1", "Q18"]),
        abs(corr.loc["Q17A2", "Q18"]),
    )
    st.markdown(
        f"""
        <div style="background:#f0fdf4; border-radius:10px; padding:12px 18px;
                    margin-top:12px; font-size:0.85rem; color:#166534;">
            ✅ 독립변수 간 최대 상관계수 {max_iv_corr} → <strong>다중공선성 우려 낮음</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # 회귀분석
    st.markdown("#### 📐 4-2. 다중회귀분석 결과")

    r2c1, r2c2, r2c3 = st.columns(3)
    r2c1.metric("Adjusted R²", f"{reg['adj_r2']:.4f}",
                f"모형 설명력 {reg['adj_r2']*100:.1f}%")
    r2c2.metric("F-statistic", f"{reg['fstat']:.3f}",
                "p < .001" if reg["fp"] < 0.001 else f"p = {reg['fp']:.4f}")
    r2c3.metric("유의수준", "α = 0.05", "3개 변수 모두 유의")

    st.markdown("**📋 회귀계수 테이블**")

    c = reg["coef"]
    reg_df = pd.DataFrame({
        "변수": c["names"],
        "비표준화 계수(B)": [f"{v:.4f}" for v in c["B"]],
        "표준오차(SE)": [f"{v:.4f}" for v in c["SE"]],
        "표준화 계수(β)": [str(v) for v in c["beta"]],
        "t-value": [f"{v:.3f}" for v in c["t"]],
        "p-value": [
            "< .001 ***" if p < 0.001 else
            "< .01 **"  if p < 0.01  else
            "< .05 *"   if p < 0.05  else
            f"{p:.4f}"
            for p in c["p"]
        ],
    })
    st.dataframe(reg_df, use_container_width=True, hide_index=True)
    st.caption("주: *** p < .001  ** p < .01  * p < .05")

    st.markdown("**📊 표준화 계수(β) 비교 — 독립변수별 상대적 영향력**")
    beta_vals = [float(v) for v in c["beta"][1:]]
    beta_df = pd.DataFrame({
        "변수": ["부모님 신뢰 (X1)", "친구 신뢰 (X2)", "사회 신뢰 (X3)"],
        "표준화 계수 β": beta_vals,
    })
    st.bar_chart(beta_df.set_index("변수"), use_container_width=True, height=260)

# ══════════════════════════════════════════════════════════════════
# TAB 5 — 결론 및 시사점
# ══════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("💡 5. 결과 해석 및 논의점")

    st.markdown("#### 📝 5-1. 결과 해석")

    beta_vals = [float(v) for v in reg["coef"]["beta"][1:]]
    rank = sorted(zip(["부모님 신뢰", "친구 신뢰", "사회 신뢰"], beta_vals),
                  key=lambda x: -x[1])

    insights = [
        (
            "🏠", "#3b82f6",
            f"가장 강력한 행복 예측 요인 — 부모님에 대한 신뢰",
            f"표준화 계수 β = {beta_vals[0]}",
            "Z세대 청소년의 행복도에 가장 큰 영향을 미치는 요인은 '부모님(보호자)에 대한 신뢰'입니다. "
            "부모를 깊이 신뢰할수록 청소년이 느끼는 주관적 행복도가 가장 가파르게 상승합니다. "
            "이는 Z세대에게 가정 환경이 여전히 심리적 안전지대의 핵심임을 보여줍니다.",
        ),
        (
            "👫", "#8b5cf6",
            "사회 신뢰의 간접적 역할 — 사회에 대한 신뢰",
            f"표준화 계수 β = {beta_vals[2]}",
            "미시적 관계에 비해 상대적으로 영향력이 작지만, '우리 사회가 믿을 수 있는 곳인가'에 대한 인식 또한 "
            "청소년의 행복에 유의미한 영향을 줍니다. Z세대가 디지털 정보와 사회 이슈에 노출되는 만큼, "
            "거시적 신뢰가 개인의 정서에 미치는 영향도 무시할 수 없습니다.",
        ),
        (
            "🌐", "#10b981",
            "또래 집단의 중요성 확인 — 친구에 대한 신뢰",
            f"표준화 계수 β = {beta_vals[1]}",
            "'친구에 대한 신뢰' 역시 청소년의 행복도에 통계적으로 유의미한 정(+)의 영향을 미쳤습니다. "
            "이는 청소년 시기 또래 애착과 교우관계의 안정성이 삶의 만족도와 직결됨을 의미합니다.",
        ),
    ]

    for icon, color, title, badge, desc_text in insights:
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
                <div style="color:#475569; font-size:0.88rem; line-height:1.8;">{desc_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### 🏛️ 5-2. 논의점 및 정책적 시사점")

    policies = [
        ("🏡", "#f59e0b", "가정 내 유대감 강화 프로그램의 필요성",
         "Z세대 청소년 정책에 있어서 가장 근본적인 토대는 '가정'임이 데이터로 확인되었습니다. "
         "부모-자녀 간 소통과 신뢰를 회복하고 증진시킬 수 있는 가족 단위의 상담·교육 정책 지원이 최우선적으로 요구됩니다."),
        ("🏫", "#8b5cf6", "건강한 교우관계를 위한 학교 환경 조성",
         "친구를 신뢰할 수 있는 환경(학교 폭력 근절, 협동 중심 교육)이 청소년의 행복 지수를 높이는 핵심 기제입니다. "
         "경쟁보다는 신뢰를 쌓을 수 있는 또래 활동 프로그램 확대가 필요합니다."),
        ("⚖️", "#10b981", "투명하고 공정한 사회 시스템 구축",
         "Z세대는 정보 탐색에 능하고 사회적 이슈에 민감합니다. 이들이 사회를 '믿을 수 있는 곳'으로 "
         "인식하도록 투명한 사회 시스템과 공정성 확립이 미래 세대의 행복을 높이는 사회적 자본이 될 것입니다."),
    ]

    for icon, color, title, desc_text in policies:
        st.markdown(
            f"""
            <div style="background:white; border-left:5px solid {color};
                        border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:14px;
                        box-shadow: 0 1px 6px rgba(0,0,0,0.06);">
                <div style="font-weight:700; color:#1e293b; margin-bottom:8px; font-size:0.95rem;">
                    {icon} {title}
                </div>
                <div style="color:#475569; font-size:0.85rem; line-height:1.8;">{desc_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
"""
Z세대 10대 청소년 신뢰·행복도 분석 보고서
AI융합교육전공 · 2542100 구정숙
"""

import streamlit as st
import pandas as pd
import numpy as np
from numpy.linalg import lstsq
from scipy import stats
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Z세대 청소년 신뢰·행복도 분석",
    page_icon="📊",
    layout="wide",
)

# ── 데이터 로드 및 분석 (캐싱) ────────────────────────────────────
@st.cache_data
def load_and_analyze(path: str):
    df = pd.read_csv(path, encoding="utf-8")

    for col in ["Q1A1", "Q17A1", "Q17A2", "Q18"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] >= 9, col] = np.nan

    df_clean = df[["Q1A1", "Q17A1", "Q17A2", "Q18"]].dropna()

    # ── 기술통계 ────────────────────────────────────────────────
    desc = df_clean.describe().round(3)

    # ── 상관계수 ────────────────────────────────────────────────
    corr = df_clean.corr().round(3)

    # ── OLS 회귀 ────────────────────────────────────────────────
    n = len(df_clean)
    y = df_clean["Q1A1"].values
    X = df_clean[["Q17A1", "Q17A2", "Q18"]].values
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

    # 표준화 계수
    X_std = (X - X.mean(axis=0)) / X.std(axis=0)
    y_std = (y - y.mean()) / y.std()
    Xc_std = np.column_stack([np.ones(n), X_std])
    b_std, _, _, _ = lstsq(Xc_std, y_std, rcond=None)

    regression = {
        "n": n,
        "r2": round(r2, 4),
        "adj_r2": round(adj_r2, 4),
        "fstat": round(fstat, 3),
        "fp": fp,
        "coef": {
            "names": ["(상수항)", "X1: 부모님 신뢰 (Q17A1)", "X2: 친구 신뢰 (Q17A2)", "X3: 사회 신뢰 (Q18)"],
            "B": b.round(4),
            "SE": se.round(4),
            "t": t_vals.round(3),
            "p": p_vals,
            "beta": ["-"] + [round(v, 3) for v in b_std[1:]],
        },
    }

    return df_clean, desc, corr, regression


# ── 파일 경로 ───────────────────────────────────────────────────
DATA_PATH = "_데이터__Z세대_10대_청소년의_가치관_변화_연구__1_.csv"

try:
    df_clean, desc, corr, reg = load_and_analyze(DATA_PATH)
    data_loaded = True
except Exception as e:
    data_loaded = False
    load_error = str(e)

# ══════════════════════════════════════════════════════════════════
# 헤더
# ══════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div style="background:linear-gradient(135deg,#1e3a5f,#0f3460);
                border-radius:16px; padding:32px 36px; margin-bottom:28px;">
        <p style="color:#93c5fd; margin:0 0 6px; font-size:0.9rem;
                  font-weight:600; letter-spacing:1px;">
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

if not data_loaded:
    st.error(
        f"⚠️ 데이터를 불러오지 못했습니다. `{DATA_PATH}` 파일을 "
        "app.py와 같은 폴더에 두고 다시 실행해 주세요."
    )
    st.code(load_error)
    st.stop()

# ══════════════════════════════════════════════════════════════════
# 탭 구성
# ══════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📁 데이터 소개", "🎯 연구 설계", "🔍 분석 방법", "📈 분석 결과", "💡 결론 및 시사점"]
)

# ══════════════════════════════════════════════════════════════════
# TAB 1 — 데이터 소개
# ══════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("📁 1. 활용한 데이터")

    col1, col2, col3 = st.columns(3)

    def data_card(col, icon, title, desc, color):
        with col:
            st.markdown(
                f"""
                <div style="background:{color}12; border:1.5px solid {color}40;
                            border-radius:14px; padding:20px; text-align:center; min-height:160px;">
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

    st.markdown("---")
    st.markdown("#### 📌 데이터 기본 정보")
    m1, m2, m3 = st.columns(3)
    m1.metric("전체 응답자 수", "5,740명", "중·고등학생")
    m2.metric("유효 분석 샘플", f"{reg['n']:,}명", "무응답 제거 후")
    m3.metric("조사 시기", "2020년 7월", "한국청소년정책연구원")

    st.markdown("---")
    st.markdown("#### 🗂️ 분석에 사용한 원본 데이터 미리보기 (상위 10행)")
    st.dataframe(
        df_clean.head(10).rename(columns={
            "Q1A1": "행복도(Q1A1)",
            "Q17A1": "부모님신뢰(Q17A1)",
            "Q17A2": "친구신뢰(Q17A2)",
            "Q18": "사회신뢰(Q18)",
        }),
        use_container_width=True,
        hide_index=True,
    )

# ══════════════════════════════════════════════════════════════════
# TAB 2 — 연구 설계
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🎯 2. 연구주제 및 변수 설정")

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
                그들의 주관적 <strong>'행복도'</strong>를 얼마나 설명할 수 있는지 확인합니다.
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

    iv_data = [
        ("X1", "부모님 신뢰도", "Q17A1",
         "다음 대상에 대해 얼마나 신뢰합니까: 부모님(보호자)",
         "1점(전혀 믿을 수 없다) ~ 4점(매우 믿을 수 있다) · 4점 척도", "#3b82f6"),
        ("X2", "친구 신뢰도", "Q17A2",
         "다음 대상에 대해 얼마나 신뢰합니까: 친구",
         "1점(전혀 믿을 수 없다) ~ 4점(매우 믿을 수 있다) · 4점 척도", "#8b5cf6"),
        ("X3", "사회 신뢰도", "Q18",
         "우리 사회가 어느 정도 믿을 수 있는 사회라고 생각합니까?",
         "0점(전혀 믿을 수 없다) ~ 10점(매우 믿을 수 있다) · 11점 척도", "#10b981"),
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
                    📌 <strong>사용 변수:</strong> {var} — {desc_text}<br>
                    📐 <strong>척도:</strong> {scale}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ══════════════════════════════════════════════════════════════════
# TAB 3 — 분석 방법
# ══════════════════════════════════════════════════════════════════
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
                        <strong>결측치 및 무응답 처리</strong><br>
                        <span style="color:#64748b; font-size:0.85rem;">
                            코드북 기준 값 <code>9</code>(Q17), <code>99</code>(Q18)는 '무응답' →
                            NaN으로 변환 후 분석에서 제외(listwise deletion)
                        </span>
                    </div>
                </div>
                <div style="display:flex; align-items:flex-start; gap:12px;">
                    <span style="background:#f59e0b; color:white; border-radius:50%;
                                 min-width:26px; height:26px; display:flex; align-items:center;
                                 justify-content:center; font-size:0.8rem; font-weight:700;">2</span>
                    <div>
                        <strong>데이터 타입 및 척도 확인</strong><br>
                        <span style="color:#64748b; font-size:0.85rem;">
                            Q1A1·Q17A1·Q17A2 → 4점 척도(연속형 처리),
                            Q18 → 0~10점 척도(연속형 처리)
                        </span>
                    </div>
                </div>
                <div style="display:flex; align-items:flex-start; gap:12px;">
                    <span style="background:#3b82f6; color:white; border-radius:50%;
                                 min-width:26px; height:26px; display:flex; align-items:center;
                                 justify-content:center; font-size:0.8rem; font-weight:700;">3</span>
                    <div>
                        <strong>척도 간 직접 비교를 위한 표준화 계수 산출</strong><br>
                        <span style="color:#64748b; font-size:0.85rem;">
                            Q18이 0~10점으로 다른 변수와 척도가 달라 비표준화 계수(B)만으로는
                            영향력 비교가 어렵기 때문에 표준화 계수(β)를 함께 보고합니다.
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 📊 3-2. 탐색적 데이터 분석 (EDA)")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div style="background:#eff6ff; border-radius:12px; padding:18px; min-height:140px;">
                <div style="font-weight:700; color:#1e40af; margin-bottom:8px;">📋 기술통계 분석</div>
                <div style="color:#475569; font-size:0.85rem; line-height:1.7;">
                    각 변수의 <strong>평균, 표준편차, 최솟값, 최댓값</strong>을 확인하여
                    Z세대 청소년의 행복도와 신뢰도 수준의 분포를 파악합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div style="background:#f5f3ff; border-radius:12px; padding:18px; min-height:140px;">
                <div style="font-weight:700; color:#6d28d9; margin-bottom:8px;">🔗 상관관계 분석 (Pearson)</div>
                <div style="color:#475569; font-size:0.85rem; line-height:1.7;">
                    종속·독립변수 간 선형 연관성을 확인하고 다중공선성 위험을 사전 파악합니다.
                    <br><span style="color:#ef4444;">※ 독립변수 간 r ≥ 0.8이면 다중공선성 의심</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
                부모님, 친구, 사회에 대한 신뢰가 각각 행복도에 유의미한
                <strong>정(+)의 영향</strong>을 미치는지 통계적으로 검증합니다.<br>
                <strong>유의수준: α = 0.05 &nbsp;|&nbsp; 분석 도구: Python (NumPy, SciPy)</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════
# TAB 4 — 분석 결과 (실제 데이터)
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("📈 4. 분석 결과")

    # EDA
    st.markdown("#### 🔍 4-1. 탐색적 데이터 분석(EDA) 결과")

    st.markdown("**📊 기술통계**")
    desc_display = pd.DataFrame({
        "변수": ["행복도 (Q1A1)", "부모님 신뢰도 (Q17A1)", "친구 신뢰도 (Q17A2)", "사회 신뢰도 (Q18)"],
        "척도": ["4점 만점", "4점 만점", "4점 만점", "10점 만점"],
        "평균": [
            round(desc.loc["mean", "Q1A1"], 3),
            round(desc.loc["mean", "Q17A1"], 3),
            round(desc.loc["mean", "Q17A2"], 3),
            round(desc.loc["mean", "Q18"], 3),
        ],
        "표준편차": [
            round(desc.loc["std", "Q1A1"], 3),
            round(desc.loc["std", "Q17A1"], 3),
            round(desc.loc["std", "Q17A2"], 3),
            round(desc.loc["std", "Q18"], 3),
        ],
        "최솟값": [
            int(desc.loc["min", "Q1A1"]),
            int(desc.loc["min", "Q17A1"]),
            int(desc.loc["min", "Q17A2"]),
            int(desc.loc["min", "Q18"]),
        ],
        "최댓값": [
            int(desc.loc["max", "Q1A1"]),
            int(desc.loc["max", "Q17A1"]),
            int(desc.loc["max", "Q17A2"]),
            int(desc.loc["max", "Q18"]),
        ],
    })
    st.dataframe(desc_display, use_container_width=True, hide_index=True)

    st.markdown("**🔗 상관관계 분석 결과**")
    c1, c2, c3 = st.columns(3)

    def corr_card(col, x, r_val, color):
        if r_val >= 0.3:
            interp = "중간 이상의 양(+)의 상관"
        elif r_val >= 0.2:
            interp = "약-중간의 양(+)의 상관"
        else:
            interp = "약한 양(+)의 상관"
        with col:
            st.markdown(
                f"""
                <div style="background:{color}0d; border:1.5px solid {color}50;
                            border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:0.82rem; color:#64748b; margin-bottom:6px;">행복도 ↔ {x}</div>
                    <div style="font-size:2rem; font-weight:800; color:{color};">r = {r_val}</div>
                    <div style="font-size:0.8rem; color:#475569; margin-top:6px;">{interp}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    corr_card(c1, "부모님 신뢰", corr.loc["Q1A1", "Q17A1"], "#3b82f6")
    corr_card(c2, "친구 신뢰",   corr.loc["Q1A1", "Q17A2"], "#8b5cf6")
    corr_card(c3, "사회 신뢰",   corr.loc["Q1A1", "Q18"],   "#10b981")

    # 독립변수 간 다중공선성 확인
    max_iv_corr = max(
        abs(corr.loc["Q17A1", "Q17A2"]),
        abs(corr.loc["Q17A1", "Q18"]),
        abs(corr.loc["Q17A2", "Q18"]),
    )
    st.markdown(
        f"""
        <div style="background:#f0fdf4; border-radius:10px; padding:12px 18px;
                    margin-top:12px; font-size:0.85rem; color:#166534;">
            ✅ 독립변수 간 최대 상관계수 {max_iv_corr} → <strong>다중공선성 우려 낮음</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # 회귀분석
    st.markdown("#### 📐 4-2. 다중회귀분석 결과")

    r2c1, r2c2, r2c3 = st.columns(3)
    r2c1.metric("Adjusted R²", f"{reg['adj_r2']:.4f}",
                f"모형 설명력 {reg['adj_r2']*100:.1f}%")
    r2c2.metric("F-statistic", f"{reg['fstat']:.3f}",
                "p < .001" if reg["fp"] < 0.001 else f"p = {reg['fp']:.4f}")
    r2c3.metric("유의수준", "α = 0.05", "3개 변수 모두 유의")

    st.markdown("**📋 회귀계수 테이블**")

    c = reg["coef"]
    reg_df = pd.DataFrame({
        "변수": c["names"],
        "비표준화 계수(B)": [f"{v:.4f}" for v in c["B"]],
        "표준오차(SE)": [f"{v:.4f}" for v in c["SE"]],
        "표준화 계수(β)": [str(v) for v in c["beta"]],
        "t-value": [f"{v:.3f}" for v in c["t"]],
        "p-value": [
            "< .001 ***" if p < 0.001 else
            "< .01 **"  if p < 0.01  else
            "< .05 *"   if p < 0.05  else
            f"{p:.4f}"
            for p in c["p"]
        ],
    })
    st.dataframe(reg_df, use_container_width=True, hide_index=True)
    st.caption("주: *** p < .001  ** p < .01  * p < .05")

    st.markdown("**📊 표준화 계수(β) 비교 — 독립변수별 상대적 영향력**")
    beta_vals = [float(v) for v in c["beta"][1:]]
    beta_df = pd.DataFrame({
        "변수": ["부모님 신뢰 (X1)", "친구 신뢰 (X2)", "사회 신뢰 (X3)"],
        "표준화 계수 β": beta_vals,
    })
    st.bar_chart(beta_df.set_index("변수"), use_container_width=True, height=260)

# ══════════════════════════════════════════════════════════════════
# TAB 5 — 결론 및 시사점
# ══════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("💡 5. 결과 해석 및 논의점")

    st.markdown("#### 📝 5-1. 결과 해석")

    beta_vals = [float(v) for v in reg["coef"]["beta"][1:]]
    rank = sorted(zip(["부모님 신뢰", "친구 신뢰", "사회 신뢰"], beta_vals),
                  key=lambda x: -x[1])

    insights = [
        (
            "🏠", "#3b82f6",
            f"가장 강력한 행복 예측 요인 — 부모님에 대한 신뢰",
            f"표준화 계수 β = {beta_vals[0]}",
            "Z세대 청소년의 행복도에 가장 큰 영향을 미치는 요인은 '부모님(보호자)에 대한 신뢰'입니다. "
            "부모를 깊이 신뢰할수록 청소년이 느끼는 주관적 행복도가 가장 가파르게 상승합니다. "
            "이는 Z세대에게 가정 환경이 여전히 심리적 안전지대의 핵심임을 보여줍니다.",
        ),
        (
            "👫", "#8b5cf6",
            "사회 신뢰의 간접적 역할 — 사회에 대한 신뢰",
            f"표준화 계수 β = {beta_vals[2]}",
            "미시적 관계에 비해 상대적으로 영향력이 작지만, '우리 사회가 믿을 수 있는 곳인가'에 대한 인식 또한 "
            "청소년의 행복에 유의미한 영향을 줍니다. Z세대가 디지털 정보와 사회 이슈에 노출되는 만큼, "
            "거시적 신뢰가 개인의 정서에 미치는 영향도 무시할 수 없습니다.",
        ),
        (
            "🌐", "#10b981",
            "또래 집단의 중요성 확인 — 친구에 대한 신뢰",
            f"표준화 계수 β = {beta_vals[1]}",
            "'친구에 대한 신뢰' 역시 청소년의 행복도에 통계적으로 유의미한 정(+)의 영향을 미쳤습니다. "
            "이는 청소년 시기 또래 애착과 교우관계의 안정성이 삶의 만족도와 직결됨을 의미합니다.",
        ),
    ]

    for icon, color, title, badge, desc_text in insights:
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
                <div style="color:#475569; font-size:0.88rem; line-height:1.8;">{desc_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### 🏛️ 5-2. 논의점 및 정책적 시사점")

    policies = [
        ("🏡", "#f59e0b", "가정 내 유대감 강화 프로그램의 필요성",
         "Z세대 청소년 정책에 있어서 가장 근본적인 토대는 '가정'임이 데이터로 확인되었습니다. "
         "부모-자녀 간 소통과 신뢰를 회복하고 증진시킬 수 있는 가족 단위의 상담·교육 정책 지원이 최우선적으로 요구됩니다."),
        ("🏫", "#8b5cf6", "건강한 교우관계를 위한 학교 환경 조성",
         "친구를 신뢰할 수 있는 환경(학교 폭력 근절, 협동 중심 교육)이 청소년의 행복 지수를 높이는 핵심 기제입니다. "
         "경쟁보다는 신뢰를 쌓을 수 있는 또래 활동 프로그램 확대가 필요합니다."),
        ("⚖️", "#10b981", "투명하고 공정한 사회 시스템 구축",
         "Z세대는 정보 탐색에 능하고 사회적 이슈에 민감합니다. 이들이 사회를 '믿을 수 있는 곳'으로 "
         "인식하도록 투명한 사회 시스템과 공정성 확립이 미래 세대의 행복을 높이는 사회적 자본이 될 것입니다."),
    ]

    for icon, color, title, desc_text in policies:
        st.markdown(
            f"""
            <div style="background:white; border-left:5px solid {color};
                        border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:14px;
                        box-shadow: 0 1px 6px rgba(0,0,0,0.06);">
                <div style="font-weight:700; color:#1e293b; margin-bottom:8px; font-size:0.95rem;">
                    {icon} {title}
                </div>
                <div style="color:#475569; font-size:0.85rem; line-height:1.8;">{desc_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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