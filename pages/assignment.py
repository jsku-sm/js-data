"""
페이지 2 — 과제
"""

import streamlit as st
import pandas as pd
import datetime


# ── 세션 상태 초기화 ────────────────────────────────────────────────
def _init_state():
    if "assignments" not in st.session_state:
        st.session_state.assignments = [
            {
                "id": 1,
                "subject": "데이터사이언스",
                "title": "Pandas 기초 실습",
                "due": datetime.date(2025, 4, 20),
                "status": "완료",
                "priority": "보통",
                "desc": "Pandas DataFrame 생성, 필터링, 집계 연산 실습",
                "file": None,
            },
            {
                "id": 2,
                "subject": "머신러닝",
                "title": "선형 회귀 모델 구현",
                "due": datetime.date(2025, 4, 28),
                "status": "진행중",
                "priority": "높음",
                "desc": "Scikit-learn으로 Boston Housing 데이터셋 예측 모델 작성",
                "file": None,
            },
            {
                "id": 3,
                "subject": "알고리즘",
                "title": "정렬 알고리즘 비교",
                "due": datetime.date(2025, 5, 5),
                "status": "예정",
                "priority": "보통",
                "desc": "버블/퀵/병합 정렬 시간복잡도 비교 보고서",
                "file": None,
            },
        ]
    if "next_id" not in st.session_state:
        st.session_state.next_id = 4


def _status_badge(status: str) -> str:
    colors = {
        "완료":  ("#dcfce7", "#166534"),
        "진행중": ("#fef9c3", "#854d0e"),
        "예정":  ("#eff6ff", "#1e40af"),
        "지연":  ("#fef2f2", "#991b1b"),
    }
    bg, fg = colors.get(status, ("#f3f4f6", "#374151"))
    return (
        f'<span style="background:{bg}; color:{fg}; padding:3px 10px; '
        f'border-radius:99px; font-size:0.8rem; font-weight:600;">{status}</span>'
    )


def _priority_badge(priority: str) -> str:
    colors = {"높음": "#ef4444", "보통": "#f59e0b", "낮음": "#22c55e"}
    color = colors.get(priority, "#6b7280")
    return (
        f'<span style="color:{color}; font-weight:700; font-size:0.85rem;">●&nbsp;{priority}</span>'
    )


def render():
    _init_state()

    # ── 헤더 ──────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#1e3a5f,#0f3460);
                    border-radius:16px; padding:32px 36px; margin-bottom:28px;">
            <h1 style="color:white; margin:0 0 6px; font-size:1.9rem;">📚 과제 관리</h1>
            <p style="color:#93c5fd; margin:0;">과제를 등록하고 진행 상황을 추적하세요</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 요약 메트릭 ───────────────────────────────────────────────
    total    = len(st.session_state.assignments)
    done     = sum(1 for a in st.session_state.assignments if a["status"] == "완료")
    inprog   = sum(1 for a in st.session_state.assignments if a["status"] == "진행중")
    upcoming = sum(1 for a in st.session_state.assignments if a["status"] == "예정")
    overdue  = sum(1 for a in st.session_state.assignments if a["status"] == "지연")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("📋 전체",   total)
    m2.metric("✅ 완료",   done,     f"+{done}")
    m3.metric("🔄 진행중", inprog)
    m4.metric("📅 예정",   upcoming)
    m5.metric("⚠️ 지연",   overdue,  f"-{overdue}" if overdue else "0")

    st.divider()

    # ── 새 과제 등록 폼 ───────────────────────────────────────────
    with st.expander("➕ 새 과제 등록", expanded=False):
        with st.form("add_assignment", clear_on_submit=True):
            fc1, fc2 = st.columns(2)
            with fc1:
                new_subject  = st.text_input("과목명 *", placeholder="예) 머신러닝")
                new_title    = st.text_input("과제 제목 *", placeholder="예) 모델 구현")
                new_due      = st.date_input("마감일 *", min_value=datetime.date.today())
            with fc2:
                new_status   = st.selectbox("상태", ["예정", "진행중", "완료", "지연"])
                new_priority = st.radio("우선순위", ["낮음", "보통", "높음"], index=1, horizontal=True)
                new_desc     = st.text_area("설명", placeholder="과제 내용을 입력하세요", height=95)

            submitted = st.form_submit_button("📌 과제 등록", type="primary", use_container_width=True)
            if submitted:
                if not new_subject or not new_title:
                    st.error("과목명과 과제 제목은 필수입니다.")
                else:
                    st.session_state.assignments.append({
                        "id":       st.session_state.next_id,
                        "subject":  new_subject,
                        "title":    new_title,
                        "due":      new_due,
                        "status":   new_status,
                        "priority": new_priority,
                        "desc":     new_desc,
                        "file":     None,
                    })
                    st.session_state.next_id += 1
                    st.success(f"✅ '{new_title}' 과제가 등록되었습니다!")
                    st.rerun()

    # ── 필터 & 검색 ───────────────────────────────────────────────
    st.subheader("📋 과제 목록")
    f1, f2, f3 = st.columns([2, 1, 1])
    with f1:
        search = st.text_input("🔍 검색", placeholder="과목명 또는 제목 검색", label_visibility="collapsed")
    with f2:
        filter_status = st.selectbox("상태 필터", ["전체", "완료", "진행중", "예정", "지연"],
                                     label_visibility="collapsed")
    with f3:
        filter_priority = st.selectbox("우선순위", ["전체", "높음", "보통", "낮음"],
                                       label_visibility="collapsed")

    # ── 필터링 ────────────────────────────────────────────────────
    filtered = st.session_state.assignments[:]
    if search:
        kw = search.lower()
        filtered = [a for a in filtered if kw in a["subject"].lower() or kw in a["title"].lower()]
    if filter_status != "전체":
        filtered = [a for a in filtered if a["status"] == filter_status]
    if filter_priority != "전체":
        filtered = [a for a in filtered if a["priority"] == filter_priority]

    if not filtered:
        st.info("검색 조건에 맞는 과제가 없습니다.")
    else:
        for a in filtered:
            today    = datetime.date.today()
            d_days   = (a["due"] - today).days
            d_label  = (
                f"🔴 D-{abs(d_days)} 지남" if d_days < 0
                else f"🟠 D-{d_days}" if d_days <= 3
                else f"🟢 D-{d_days}"
            )

            with st.container():
                st.markdown(
                    f"""
                    <div style="border:1px solid #e2e8f0; border-radius:12px;
                                padding:16px 20px; margin-bottom:12px; background:#fafafa;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
                            <div>
                                <span style="font-size:0.78rem; color:#6b7280;">{a['subject']}</span>
                                <h4 style="margin:2px 0 6px; font-size:1.05rem;">{a['title']}</h4>
                                <span style="font-size:0.82rem; color:#64748b;">{a['desc'] or '설명 없음'}</span>
                            </div>
                            <div style="display:flex; flex-direction:column; align-items:flex-end; gap:6px;">
                                {_status_badge(a['status'])}
                                {_priority_badge(a['priority'])}
                                <span style="font-size:0.8rem; color:#64748b;">📅 {a['due']} &nbsp;{d_label}</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                c_up, c_del, c_stat = st.columns([2, 1, 1])
                with c_up:
                    uploaded_file = st.file_uploader(
                        f"파일 첨부 (ID:{a['id']})",
                        key=f"file_{a['id']}",
                        label_visibility="collapsed",
                    )
                    if uploaded_file:
                        a["file"] = uploaded_file.name
                        st.success(f"📎 {uploaded_file.name} 첨부 완료")
                with c_stat:
                    new_s = st.selectbox(
                        "상태 변경",
                        ["예정", "진행중", "완료", "지연"],
                        index=["예정", "진행중", "완료", "지연"].index(a["status"]),
                        key=f"sel_{a['id']}",
                        label_visibility="collapsed",
                    )
                    if new_s != a["status"]:
                        a["status"] = new_s
                        st.rerun()
                with c_del:
                    if st.button("🗑️ 삭제", key=f"del_{a['id']}", use_container_width=True):
                        st.session_state.assignments = [
                            x for x in st.session_state.assignments if x["id"] != a["id"]
                        ]
                        st.rerun()

    # ── 진행률 요약 ───────────────────────────────────────────────
    st.divider()
    st.subheader("📈 전체 진행률")
    if total > 0:
        rate = done / total
        st.progress(rate, text=f"{done}/{total}개 완료 ({rate*100:.0f}%)")

    # ── 엑셀 내보내기 ─────────────────────────────────────────────
    st.divider()
    st.subheader("📥 데이터 내보내기")
    if st.button("📊 과제 목록 CSV 다운로드", use_container_width=True):
        df_export = pd.DataFrame([
            {k: v for k, v in a.items() if k != "file"}
            for a in st.session_state.assignments
        ])
        st.download_button(
            label="⬇️ CSV 저장",
            data=df_export.to_csv(index=False, encoding="utf-8-sig"),
            file_name="assignments.csv",
            mime="text/csv",
            use_container_width=True,
        )
