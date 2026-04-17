import streamlit as st
import pandas as pd
import numpy as np
import pyreadstat
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import os
import warnings
warnings.filterwarnings('ignore')

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(
    page_title="청소년 금융이해력 분석",
    page_icon="📊",
    layout="wide"
)

# ── 한글 폰트 설정 ───────────────────────────────────────
@st.cache_resource
def set_korean_font():
    font_candidates = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "C:/Windows/Fonts/malgun.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    ]
    for path in font_candidates:
        if os.path.exists(path):
            fm.fontManager.addfont(path)
            prop = fm.FontProperties(fname=path)
            plt.rcParams['font.family'] = prop.get_name()
            plt.rcParams['axes.unicode_minus'] = False
            return prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
    return None

font_name = set_korean_font()

# ── 데이터 로드 ──────────────────────────────────────────
@st.cache_data
def load_data(uploaded_file):
    with open("temp_data.sav", "wb") as f:
        f.write(uploaded_file.read())
    df, meta = pyreadstat.read_sav("temp_data.sav")
    os.remove("temp_data.sav")
    return df, meta

# ── 전처리 함수 ──────────────────────────────────────────
@st.cache_data
def preprocess(df):
    knowledge_cols = ['Q02', 'Q03', 'Q04', 'Q05', 'Q06', 'Q07', 'Q08']
    behavior_cols  = ['Q09', 'Q0901', 'Q11', 'Q12', 'Q13', 'Q14']

    df2 = df.copy()
    df2['financial_literacy_score'] = (
        df2[knowledge_cols].sum(axis=1) + df2[behavior_cols].sum(axis=1)
    )

    # Q26 합산
    q26_cols = ['Q26', 'Q2601', 'Q2602', 'Q2603', 'Q2604', 'Q2605', 'Q2606']
    existing = [c for c in q26_cols if c in df2.columns]
    df2['Q26'] = df2[existing].sum(axis=1)

    # Q33 합산
    q33_cols = ['Q33', 'Q3301', 'Q3302', 'Q3303', 'Q3304']
    existing33 = [c for c in q33_cols if c in df2.columns]
    df2['Q33'] = df2[existing33].sum(axis=1)

    # 결측치 제거
    df2 = df2.dropna(subset=['Q26', 'Q27', 'Q33', 'financial_literacy_score'])

    # Q27 더미화
    df2 = pd.get_dummies(df2, columns=['Q27'], drop_first=True)
    q27_col = [c for c in df2.columns if 'Q27_' in c][0]

    return df2, q27_col

# ── 사이드바 ─────────────────────────────────────────────
st.sidebar.title("📂 데이터 업로드")
uploaded_file = st.sidebar.file_uploader(
    "SAV 파일을 업로드하세요",
    type=["sav"],
    help="2023 청소년 금융이해력 조사 중고등학생 데이터"
)

# ── 메인 타이틀 ──────────────────────────────────────────
st.title("📊 청소년 금융이해력 다중회귀분석")
st.markdown("""
**연구주제**: 중·고등학생의 부모 금융교육이 청소년 금융이해력에 미치는 영향

| 구분 | 변수 | 설명 |
|------|------|------|
| 종속변수 | 금융이해력 종합점수 | Q02~Q14 합산 |
| 독립변수 1 | 부모 금융교육 수준 | Q26 (7문항 합산) |
| 독립변수 2 | 학교 금융교육 경험 | Q27 (더미변수) |
| 독립변수 3 | 금융 웰빙 | Q33 (5문항 합산) |
""")

st.divider()

# ── 데이터 없을 때 ───────────────────────────────────────
if uploaded_file is None:
    st.info("👈 왼쪽에서 SAV 파일을 업로드하면 분석이 시작됩니다!")
    st.stop()

# ── 데이터 로드 & 전처리 ─────────────────────────────────
with st.spinner("데이터를 불러오는 중..."):
    df_raw, meta = load_data(uploaded_file)
    df, q27_col = preprocess(df_raw)

st.success(f"✅ 데이터 로드 완료! 총 {len(df_raw)}명 → 결측치 제거 후 **{len(df)}명** 사용")

# ── 탭 구성 ──────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📋 데이터 미리보기", "📈 분포 확인", "🔍 다중공선성", "📉 회귀분석 결과"])

# ── TAB 1: 데이터 미리보기 ───────────────────────────────
with tab1:
    st.subheader("데이터 미리보기 (상위 5행)")
    cols_show = ['financial_literacy_score', 'Q26', 'Q33', q27_col]
    st.dataframe(df[cols_show].head(), use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("표본 수", f"{len(df):,}명")
    col2.metric("금융이해력 평균", f"{df['financial_literacy_score'].mean():.2f}점")
    col3.metric("부모교육 평균", f"{df['Q26'].mean():.2f}점")
    col4.metric("금융웰빙 평균", f"{df['Q33'].mean():.2f}점")

# ── TAB 2: 분포 확인 ─────────────────────────────────────
with tab2:
    st.subheader("변수별 분포")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.patch.set_facecolor('white')

    plot_vars = [
        ('financial_literacy_score', '금융이해력 종합점수', '#4C72B0'),
        ('Q26', '부모 금융교육 수준', '#55A868'),
        ('Q33', '금융 웰빙', '#C44E52'),
    ]

    for ax, (col, label, color) in zip(axes, plot_vars):
        ax.hist(df[col].dropna(), bins=20, color=color, alpha=0.7, edgecolor='white')
        ax.set_title(label, fontsize=12, fontweight='bold')
        ax.set_xlabel('점수')
        ax.set_ylabel('빈도')
        mean_val = df[col].mean()
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'평균: {mean_val:.1f}')
        ax.legend(fontsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)

    # Q27 막대그래프
    st.subheader("학교 금융교육 경험 분포 (Q27)")
    fig2, ax2 = plt.subplots(figsize=(5, 3))
    counts = df[q27_col].value_counts().sort_index()
    labels = ['없음 (0)', '있음 (1)']
    ax2.bar(labels, counts.values, color=['#C44E52', '#4C72B0'], alpha=0.8, width=0.4)
    for i, v in enumerate(counts.values):
        ax2.text(i, v + 10, f'{v:,}명\n({v/len(df)*100:.1f}%)', ha='center', fontsize=10)
    ax2.set_ylabel('명')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig2)

# ── TAB 3: 다중공선성 ────────────────────────────────────
with tab3:
    st.subheader("다중공선성 확인 (VIF)")
    st.markdown("VIF 값이 **10 이하**이면 다중공선성 문제가 없다고 판단해요.")

    X_vif = df[['Q26', 'Q33', q27_col]].dropna().astype(float)
    X_vif_const = sm.add_constant(X_vif)

    vif_data = pd.DataFrame({
        '변수': ['Q26 (부모 금융교육)', 'Q33 (금융 웰빙)', 'Q27 (학교 금융교육)'],
        'VIF': [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
    })
    vif_data['판정'] = vif_data['VIF'].apply(lambda x: '✅ 문제없음' if x < 10 else '⚠️ 주의')

    st.dataframe(vif_data, use_container_width=True, hide_index=True)

    # VIF 시각화
    fig3, ax3 = plt.subplots(figsize=(6, 3))
    colors = ['#55A868' if v < 10 else '#C44E52' for v in vif_data['VIF']]
    bars = ax3.barh(vif_data['변수'], vif_data['VIF'], color=colors, alpha=0.8)
    ax3.axvline(10, color='red', linestyle='--', linewidth=1.5, label='기준선 (VIF=10)')
    ax3.set_xlabel('VIF 값')
    for bar, val in zip(bars, vif_data['VIF']):
        ax3.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                 f'{val:.2f}', va='center', fontsize=10)
    ax3.legend()
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig3)

# ── TAB 4: 회귀분석 결과 ─────────────────────────────────
with tab4:
    st.subheader("다중선형회귀분석 결과")

    X = df[['Q26', 'Q33', q27_col]].astype(float)
    y = df['financial_literacy_score'].astype(float)
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()

    # 핵심 지표
    col1, col2, col3 = st.columns(3)
    col1.metric("R² (설명력)", f"{model.rsquared:.4f}")
    col2.metric("수정된 R²", f"{model.rsquared_adj:.4f}")
    col3.metric("F통계량 p값", f"{model.f_pvalue:.2e}")

    if model.f_pvalue < 0.05:
        st.success("✅ 모델이 통계적으로 유의미합니다! (p < 0.05)")
    else:
        st.warning("⚠️ 모델이 통계적으로 유의미하지 않습니다.")

    st.divider()

    # 회귀계수 표
    st.subheader("📋 회귀계수 상세 결과")
    result_df = pd.DataFrame({
        '변수': ['상수(const)', '부모 금융교육(Q26)', '금융 웰빙(Q33)', '학교 금융교육(Q27)'],
        '회귀계수': model.params.values,
        '표준오차': model.bse.values,
        't값': model.tvalues.values,
        'p값': model.pvalues.values,
        '95% CI 하한': model.conf_int()[0].values,
        '95% CI 상한': model.conf_int()[1].values,
    })
    result_df['유의성'] = result_df['p값'].apply(
        lambda p: '✅ 유의 (p<0.05)' if p < 0.05 else '❌ 비유의'
    )

    st.dataframe(
        result_df.style.format({
            '회귀계수': '{:.4f}', '표준오차': '{:.4f}',
            't값': '{:.3f}', 'p값': '{:.4f}',
            '95% CI 하한': '{:.4f}', '95% CI 상한': '{:.4f}'
        }),
        use_container_width=True, hide_index=True
    )

    # 회귀계수 시각화
    st.divider()
    st.subheader("📊 회귀계수 시각화")

    coef_df = result_df[result_df['변수'] != '상수(const)'].copy()
    colors_bar = ['#55A868' if p < 0.05 else '#AAAAAA' for p in coef_df['p값']]

    fig4, ax4 = plt.subplots(figsize=(7, 4))
    bars = ax4.barh(coef_df['변수'], coef_df['회귀계수'], color=colors_bar, alpha=0.85)
    ax4.axvline(0, color='black', linewidth=0.8)
    for bar, lo, hi in zip(bars, coef_df['95% CI 하한'], coef_df['95% CI 상한']):
        y_pos = bar.get_y() + bar.get_height() / 2
        ax4.plot([lo, hi], [y_pos, y_pos], color='black', linewidth=2)
    ax4.set_xlabel('회귀계수 (95% 신뢰구간 포함)')
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#55A868', alpha=0.85, label='통계적으로 유의미 (p<0.05)'),
        Patch(facecolor='#AAAAAA', alpha=0.85, label='유의미하지 않음')
    ]
    ax4.legend(handles=legend_elements, loc='lower right', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig4)

    # 결과 해석
    st.divider()
    st.subheader("💡 결과 해석")

    q26_p = model.pvalues['Q26']
    q33_p = model.pvalues['Q33']
    q27_p = model.pvalues[q27_col]

    if q26_p < 0.05:
        st.success(f"**부모 금융교육(Q26)**: 회귀계수 {model.params['Q26']:.4f}, p={q26_p:.4f} → ✅ 유의미! 부모 금융교육 수준이 높을수록 금융이해력이 높아져요.")
    else:
        st.warning(f"**부모 금융교육(Q26)**: p={q26_p:.4f} → ❌ 유의미하지 않음")

    if q33_p < 0.05:
        st.success(f"**금융 웰빙(Q33)**: 회귀계수 {model.params['Q33']:.4f}, p={q33_p:.4f} → ✅ 유의미!")
    else:
        st.info(f"**금융 웰빙(Q33)**: 회귀계수 {model.params['Q33']:.4f}, p={q33_p:.4f} → ❌ 이 모델에서는 유의미하지 않아요.")

    if q27_p < 0.05:
        st.success(f"**학교 금융교육(Q27)**: 회귀계수 {model.params[q27_col]:.4f}, p={q27_p:.4f} → ✅ 유의미! 학교 금융교육 경험이 있는 학생이 점수가 더 높아요.")
    else:
        st.warning(f"**학교 금융교육(Q27)**: p={q27_p:.4f} → ❌ 유의미하지 않음")