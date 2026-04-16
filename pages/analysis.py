"""
페이지 3 — 데이터 분석
"""

import streamlit as st
import pandas as pd
import numpy as np


# ── 샘플 데이터 생성 ─────────────────────────────────────────────────
@st.cache_data
def _make_sample() -> pd.DataFrame:
    np.random.seed(42)
    n = 200
    return pd.DataFrame({
        "학번":    [f"2024{i:04d}" for i in range(1, n + 1)],
        "이름":    [f"학생{i:03d}"  for i in range(1, n + 1)],
        "학과":    np.random.choice(["컴퓨터공학", "통계학", "수학", "물리학", "화학"], n),
        "학년":    np.random.choice([1, 2, 3, 4], n),
        "학점":    np.round(np.random.normal(3.2, 0.5, n).clip(0, 4.5), 2),
        "출석률":  np.round(np.random.uniform(60, 100, n), 1),
        "과제점수": np.random.randint(50, 100, n),
        "시험점수": np.random.randint(40, 100, n),
        "성별":    np.random.choice(["남", "여"], n),
    })


def render():
    # ── 헤더 ──────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#134e4a,#0f3460);
                    border-radius:16px; padding:32px 36px; margin-bottom:28px;">
            <h1 style="color:white; margin:0 0 6px; font-size:1.9rem;">📊 데이터 분석</h1>
            <p style="color:#6ee7b7; margin:0;">CSV 파일을 업로드하거나 샘플 데이터로 분석을 시작하세요</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 데이터 로드 ───────────────────────────────────────────────
    st.subheader("📂 데이터 불러오기")
    load_col1, load_col2 = st.columns([3, 1], gap="large")

    with load_col1:
        uploaded = st.file_uploader(
            "CSV 또는 Excel 파일을 업로드하세요",
            type=["csv", "xlsx", "xls"],
            help="인코딩은 UTF-8 또는 EUC-KR을 지원합니다.",
        )

    with load_col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        use_sample = st.button("🎲 샘플 데이터 사용", use_container_width=True, type="primary")

    # ── 데이터프레임 결정 ─────────────────────────────────────────
    if "df" not in st.session_state:
        st.session_state.df = None

    if use_sample:
        st.session_state.df = _make_sample()
        st.success("✅ 샘플 데이터(200행 × 9열)를 불러왔습니다.")

    if uploaded is not None:
        try:
            if uploaded.name.endswith(".csv"):
                for enc in ["utf-8", "utf-8-sig", "euc-kr", "cp949"]:
                    try:
                        uploaded.seek(0)
                        df_tmp = pd.read_csv(uploaded, encoding=enc)
                        break
                    except Exception:
                        continue
            else:
                df_tmp = pd.read_excel(uploaded)
            st.session_state.df = df_tmp
            st.success(f"✅ '{uploaded.name}' 로드 완료 — {df_tmp.shape[0]:,}행 × {df_tmp.shape[1]}열")
        except Exception as e:
            st.error(f"파일 읽기 실패: {e}")

    df = st.session_state.df

    if df is None:
        st.info("👆 파일을 업로드하거나 샘플 데이터를 선택하세요.")
        return

    # ══════════════════════════════════════════════════════════════
    # 탭 구성
    # ══════════════════════════════════════════════════════════════
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔍 데이터 탐색", "📈 시각화", "🧮 통계 분석", "💾 내보내기"]
    )

    # ──────────────────────────────────────────────────────────────
    # TAB 1 — 데이터 탐색
    # ──────────────────────────────────────────────────────────────
    with tab1:
        # 기본 정보
        i1, i2, i3, i4 = st.columns(4)
        i1.metric("총 행 수",   f"{df.shape[0]:,}")
        i2.metric("총 열 수",   df.shape[1])
        i3.metric("결측값",     int(df.isnull().sum().sum()))
        i4.metric("중복 행",    int(df.duplicated().sum()))

        st.divider()

        # 데이터프레임 뷰어
        st.subheader("📋 데이터 미리보기")
        c_rows, c_search = st.columns([1, 2])
        with c_rows:
            show_rows = st.slider("표시 행 수", 5, min(100, len(df)), 10)
        with c_search:
            col_filter = st.multiselect(
                "표시 열 선택 (기본: 전체)",
                df.columns.tolist(),
                default=[],
                placeholder="열을 선택하거나 비워두면 전체 표시",
            )

        view_df = df[col_filter] if col_filter else df
        st.dataframe(view_df.head(show_rows), use_container_width=True)

        st.divider()

        # 컬럼 정보
        st.subheader("🗂️ 열(컬럼) 정보")
        col_info = pd.DataFrame({
            "열 이름":  df.columns,
            "데이터타입": df.dtypes.astype(str).values,
            "결측값 수":  df.isnull().sum().values,
            "결측률(%)":  (df.isnull().mean() * 100).round(1).values,
            "고유값 수":  df.nunique().values,
        })
        st.dataframe(col_info, use_container_width=True, hide_index=True)

    # ──────────────────────────────────────────────────────────────
    # TAB 2 — 시각화
    # ──────────────────────────────────────────────────────────────
    with tab2:
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

        chart_type = st.selectbox(
            "차트 유형 선택",
            ["📊 막대 차트", "📈 선 차트", "🔵 산점도", "📐 히스토그램", "🥧 범주 분포"],
        )

        # ── 막대 차트 ──
        if chart_type == "📊 막대 차트":
            st.subheader("막대 차트")
            v1, v2 = st.columns(2)
            with v1:
                x_col = st.selectbox("X축 (범주형)", cat_cols if cat_cols else df.columns.tolist())
            with v2:
                y_col = st.selectbox("Y축 (수치형)", num_cols if num_cols else df.columns.tolist())
            agg_df = df.groupby(x_col)[y_col].mean().reset_index()
            agg_df.columns = [x_col, f"{y_col} 평균"]
            st.bar_chart(agg_df.set_index(x_col), use_container_width=True, height=350)

        # ── 선 차트 ──
        elif chart_type == "📈 선 차트":
            st.subheader("선 차트")
            y_cols = st.multiselect("Y축 열 선택", num_cols, default=num_cols[:2] if len(num_cols) >= 2 else num_cols)
            if y_cols:
                st.line_chart(df[y_cols].reset_index(drop=True), use_container_width=True, height=350)

        # ── 산점도 ──
        elif chart_type == "🔵 산점도":
            st.subheader("산점도")
            sc1, sc2 = st.columns(2)
            with sc1:
                sx = st.selectbox("X축", num_cols, index=0)
            with sc2:
                sy = st.selectbox("Y축", num_cols, index=min(1, len(num_cols) - 1))
            color_col = None
            if cat_cols:
                color_col = st.selectbox("색상 구분 (선택)", ["없음"] + cat_cols)
                color_col = None if color_col == "없음" else color_col
            scatter_df = df[[sx, sy] + ([color_col] if color_col else [])].dropna()
            st.scatter_chart(scatter_df, x=sx, y=sy, color=color_col, use_container_width=True, height=380)

        # ── 히스토그램 ──
        elif chart_type == "📐 히스토그램":
            st.subheader("히스토그램")
            h_col  = st.selectbox("열 선택", num_cols)
            h_bins = st.slider("구간(bins) 수", 5, 80, 20)
            series = df[h_col].dropna()
            counts, edges = np.histogram(series, bins=h_bins)
            hist_df = pd.DataFrame({
                "구간": [f"{edges[i]:.1f}~{edges[i+1]:.1f}" for i in range(len(counts))],
                "빈도": counts,
            })
            st.bar_chart(hist_df.set_index("구간"), use_container_width=True, height=350)
            st.caption(f"평균: {series.mean():.2f} | 표준편차: {series.std():.2f} | 중앙값: {series.median():.2f}")

        # ── 범주 분포 ──
        elif chart_type == "🥧 범주 분포":
            st.subheader("범주별 분포")
            if not cat_cols:
                st.warning("범주형 열이 없습니다.")
            else:
                cat_sel = st.selectbox("범주형 열 선택", cat_cols)
                vc = df[cat_sel].value_counts().reset_index()
                vc.columns = [cat_sel, "count"]
                st.bar_chart(vc.set_index(cat_sel), use_container_width=True, height=320)

                # 비율 표
                vc["비율(%)"] = (vc["count"] / vc["count"].sum() * 100).round(1)
                st.dataframe(vc, use_container_width=True, hide_index=True)

    # ──────────────────────────────────────────────────────────────
    # TAB 3 — 통계 분석
    # ──────────────────────────────────────────────────────────────
    with tab3:
        st.subheader("📊 기술 통계")
        num_df = df.select_dtypes(include=np.number)
        if num_df.empty:
            st.warning("수치형 열이 없습니다.")
        else:
            desc = num_df.describe().T.round(3)
            desc.index.name = "열"
            st.dataframe(desc, use_container_width=True)

        st.divider()

        # ── 상관 분석 ──
        st.subheader("🔗 상관 분석 (Correlation)")
        if len(num_df.columns) < 2:
            st.info("수치형 열이 2개 이상 필요합니다.")
        else:
            corr = num_df.corr().round(3)
            st.dataframe(
                corr.style.background_gradient(cmap="RdYlGn", axis=None, vmin=-1, vmax=1),
                use_container_width=True,
            )

            # 가장 상관 높은 쌍
            st.subheader("🔍 주요 상관 쌍")
            pairs = []
            cols_list = corr.columns.tolist()
            for i in range(len(cols_list)):
                for j in range(i + 1, len(cols_list)):
                    pairs.append({
                        "열 A":    cols_list[i],
                        "열 B":    cols_list[j],
                        "상관계수": corr.iloc[i, j],
                    })
            pairs_df = pd.DataFrame(pairs).sort_values("상관계수", ascending=False, key=abs)
            st.dataframe(pairs_df.head(10), use_container_width=True, hide_index=True)

        st.divider()

        # ── 그룹별 집계 ──
        st.subheader("📦 그룹별 집계")
        cat_cols_list = df.select_dtypes(exclude=np.number).columns.tolist()
        if not cat_cols_list or num_df.empty:
            st.info("범주형 열과 수치형 열이 모두 필요합니다.")
        else:
            g1, g2, g3 = st.columns(3)
            with g1:
                grp_by  = st.selectbox("그룹 기준 열", cat_cols_list, key="grp_by")
            with g2:
                grp_val = st.selectbox("집계 대상 열", num_df.columns.tolist(), key="grp_val")
            with g3:
                grp_fn  = st.selectbox("집계 함수", ["평균", "합계", "최대", "최소", "개수"])

            fn_map = {"평균": "mean", "합계": "sum", "최대": "max", "최소": "min", "개수": "count"}
            grp_result = df.groupby(grp_by)[grp_val].agg(fn_map[grp_fn]).reset_index()
            grp_result.columns = [grp_by, f"{grp_val}_{grp_fn}"]

            st.dataframe(grp_result, use_container_width=True, hide_index=True)
            st.bar_chart(grp_result.set_index(grp_by), use_container_width=True, height=280)

    # ──────────────────────────────────────────────────────────────
    # TAB 4 — 내보내기
    # ──────────────────────────────────────────────────────────────
    with tab4:
        st.subheader("💾 분석 결과 내보내기")

        e1, e2 = st.columns(2)

        with e1:
            st.markdown("**📄 원본 데이터 CSV 저장**")
            csv_data = df.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="⬇️ 원본 데이터 다운로드 (CSV)",
                data=csv_data,
                file_name="data_export.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with e2:
            st.markdown("**📊 기술통계 CSV 저장**")
            num_df2 = df.select_dtypes(include=np.number)
            if not num_df2.empty:
                stat_csv = num_df2.describe().T.round(3).to_csv(encoding="utf-8-sig")
                st.download_button(
                    label="⬇️ 기술통계 다운로드 (CSV)",
                    data=stat_csv,
                    file_name="statistics.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            else:
                st.info("수치형 열이 없어 통계를 내보낼 수 없습니다.")

        st.divider()
        st.subheader("📝 분석 메모")
        memo = st.text_area(
            "분석 내용이나 인사이트를 기록하세요",
            placeholder="예) 학점과 출석률 사이에 0.72의 양의 상관관계가 확인됨...",
            height=160,
        )
        if memo:
            st.download_button(
                label="📥 메모 저장 (.txt)",
                data=memo,
                file_name="analysis_memo.txt",
                mime="text/plain",
                use_container_width=True,
            )
