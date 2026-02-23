"""
╔══════════════════════════════════════════════════════════╗
║          ELITE FITNESS TRACKING DASHBOARD                ║
║    Progressive Overload · Body Recomposition · Health    ║
╚══════════════════════════════════════════════════════════╝
Run: streamlit run app.py
Access on phone: http://<your-local-ip>:8501
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# CONFIG & SETUP
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Elite Fitness Dashboard",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_DIR = "fitness_data"
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "workout":    os.path.join(DATA_DIR, "workouts.json"),
    "pr":         os.path.join(DATA_DIR, "pr_tracker.json"),
    "body":       os.path.join(DATA_DIR, "body_metrics.json"),
    "nutrition":  os.path.join(DATA_DIR, "nutrition.json"),
    "recovery":   os.path.join(DATA_DIR, "recovery.json"),
    "supplement": os.path.join(DATA_DIR, "supplements.json"),
    "hormone":    os.path.join(DATA_DIR, "hormone.json"),
}

def load(key):
    if os.path.exists(FILES[key]):
        with open(FILES[key]) as f:
            return json.load(f)
    return []


def save(key, data):
    with open(FILES[key], "w") as f:
        json.dump(data, f, indent=2, default=str)


def to_df(key):
    data = load(key)
    return pd.DataFrame(data) if data else pd.DataFrame()

# ─────────────────────────────────────────────
# GLOBAL STYLES  (mobile-first responsive)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* dark background */
.stApp { background: #0d0f14; color: #e8eaf0; }

/* ── Nav pill tabs ── */
div[data-testid="stHorizontalBlock"] { gap: 6px !important; }

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, #1a1d2e 0%, #12151f 100%);
    border: 1px solid #2a2d3e;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.metric-card h3 { margin: 0 0 4px; font-size: 0.78rem; color: #7c8db5; text-transform: uppercase; letter-spacing: 1px; }
.metric-card .value { font-size: 2rem; font-weight: 900; color: #fff; line-height: 1.1; }
.metric-card .delta { font-size: 0.8rem; margin-top: 4px; }
.delta-up   { color: #4ade80; }
.delta-down { color: #f87171; }

/* ── Section headers ── */
.section-header {
    font-size: 1.3rem; font-weight: 700; color: #c7d2fe;
    border-left: 4px solid #6366f1; padding-left: 12px;
    margin: 24px 0 16px;
}

/* ── Pill tag ── */
.pill {
    display: inline-block; padding: 3px 12px; border-radius: 999px;
    font-size: 0.75rem; font-weight: 600; margin: 2px;
}
.pill-green  { background:#14532d; color:#4ade80; }
.pill-blue   { background:#1e3a5f; color:#60a5fa; }
.pill-purple { background:#2e1065; color:#c084fc; }
.pill-orange { background:#431407; color:#fb923c; }

/* ── Form containers ── */
.form-box {
    background: #13161f;
    border: 1px solid #252838;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
}

/* ── PR badge ── */
.pr-badge {
    background: linear-gradient(135deg,#7c3aed,#4f46e5);
    border-radius: 12px; padding: 14px 18px;
    margin-bottom: 10px; display: flex; justify-content: space-between;
    align-items: center;
}
.pr-badge .ex { font-weight: 700; font-size: 1rem; }
.pr-badge .stats { font-size: 0.85rem; color: #c4b5fd; text-align: right; }

/* ── Table ── */
.dataframe thead th { background: #1a1d2e !important; color: #a5b4fc !important; }
.dataframe tbody tr:nth-child(even) { background: #12151f !important; }

/* ── Plotly charts ── */
.js-plotly-plot { border-radius: 12px; overflow: hidden; }

/* ── Streamlit tweaks ── */
.stSelectbox > div > div { background: #13161f !important; border-color: #2a2d3e !important; }
.stTextInput > div > div { background: #13161f !important; border-color: #2a2d3e !important; }
.stNumberInput > div > div { background: #13161f !important; border-color: #2a2d3e !important; }
.stTextArea > div > div { background: #13161f !important; border-color: #2a2d3e !important; }
.stButton > button {
    background: linear-gradient(135deg,#6366f1,#4f46e5) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    padding: 10px 20px !important; width: 100%;
}
.stButton > button:hover { opacity: 0.9; transform: translateY(-1px); }
div[data-testid="stSlider"] .rc-slider-handle { background:#6366f1 !important; border-color:#6366f1 !important; }
div[data-testid="stSlider"] .rc-slider-track { background:#6366f1 !important; }

/* ── Mobile responsive ── */
@media (max-width: 768px) {
    .metric-card .value { font-size: 1.5rem; }
    .section-header { font-size: 1.1rem; }
    .pr-badge { flex-direction: column; gap: 6px; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 10px 0 20px;">
    <div style="font-size:2rem; font-weight:900; background: linear-gradient(135deg,#6366f1,#a78bfa,#38bdf8);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1.1;">
        🏋️ ELITE FITNESS OS
    </div>
    <div style="color:#7c8db5; font-size:0.85rem; margin-top:4px;">
        Progressive Overload · Body Recomposition · Longevity
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────
PAGES = ["📊 Dashboard", "🏋️ Workout", "🏆 PRs", "📏 Body", "🥗 Nutrition", "😴 Recovery", "💊 Supplements", "🧬 Hormones"]

if "page" not in st.session_state:
    st.session_state.page = "📊 Dashboard"

cols = st.columns(len(PAGES))
for i, p in enumerate(PAGES):
    with cols[i]:
        if st.button(p, key=f"nav_{i}", use_container_width=True):
            st.session_state.page = p

page = st.session_state.page
st.markdown("---")


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════
CHART_LAYOUT = dict(
    paper_bgcolor="#0d0f14", plot_bgcolor="#0d0f14",
    font_color="#e8eaf0", margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(bgcolor="#13161f", bordercolor="#2a2d3e"),
    xaxis=dict(gridcolor="#1e2133", zerolinecolor="#1e2133"),
    yaxis=dict(gridcolor="#1e2133", zerolinecolor="#1e2133"),
)

COLORS = ["#6366f1", "#38bdf8", "#4ade80", "#f87171", "#fb923c", "#c084fc", "#facc15"]


def sparkline(df, col, title="", color="#6366f1"):
    if df.empty or col not in df.columns:
        return None
    fig = px.line(df, y=col, color_discrete_sequence=[color])
    fig.update_traces(line_width=2, fill="tozeroy",
                      fillcolor=f"rgba{tuple(list(px.colors.hex_to_rgb(color)) + [0.1])}")
    fig.update_layout(**CHART_LAYOUT, height=80, showlegend=False,
                      xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig


def card(title, value, unit="", delta=None, color="#6366f1"):
    delta_html = ""
    if delta is not None:
        cls = "delta-up" if delta >= 0 else "delta-down"
        arrow = "▲" if delta >= 0 else "▼"
        delta_html = f'<div class="delta {cls}">{arrow} {abs(delta):.1f} {unit}</div>'
    st.markdown(f"""
    <div class="metric-card" style="border-top: 3px solid {color}">
        <h3>{title}</h3>
        <div class="value">{value}<span style="font-size:0.9rem;color:#7c8db5;font-weight:500"> {unit}</span></div>
        {delta_html}
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    today = date.today().isoformat()
    st.markdown('<div class="section-header">📅 Today at a Glance</div>', unsafe_allow_html=True)

    # Pull latest records
    wdf = to_df("workout")
    bdf = to_df("body")
    ndf = to_df("nutrition")
    rdf = to_df("recovery")
    sdf = to_df("supplement")
    hdf = to_df("hormone")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        bw = bdf["bodyweight"].iloc[-1] if not bdf.empty and "bodyweight" in bdf else "–"
        delta_bw = None
        if not bdf.empty and len(bdf) > 1:
            delta_bw = float(bdf["bodyweight"].iloc[-1]) - float(bdf["bodyweight"].iloc[-2])
        card("⚖️ Bodyweight", bw, "kg", delta_bw, "#6366f1")
    with c2:
        cal = ndf["calories"].iloc[-1] if not ndf.empty and "calories" in ndf else "–"
        card("🔥 Calories", cal, "kcal", color="#f87171")
    with c3:
        prot = ndf["protein"].iloc[-1] if not ndf.empty and "protein" in ndf else "–"
        card("🥩 Protein", prot, "g", color="#4ade80")
    with c4:
        slp = rdf["sleep_hours"].iloc[-1] if not rdf.empty and "sleep_hours" in rdf else "–"
        card("😴 Sleep", slp, "hrs", color="#38bdf8")

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        steps = hdf["daily_steps"].iloc[-1] if not hdf.empty and "daily_steps" in hdf else "–"
        card("👟 Steps", steps, "", color="#fb923c")
    with c6:
        water = ndf["water_l"].iloc[-1] if not ndf.empty and "water_l" in ndf else "–"
        card("💧 Water", water, "L", color="#38bdf8")
    with c7:
        stress = rdf["stress_level"].iloc[-1] if not rdf.empty and "stress_level" in rdf else "–"
        card("🧠 Stress", stress, "/5", color="#f87171")
    with c8:
        energy = rdf["energy_level"].iloc[-1] if not rdf.empty and "energy_level" in rdf else "–"
        card("⚡ Energy", energy, "/5", color="#facc15")

    # Supplement checklist today
    st.markdown('<div class="section-header">💊 Supplement Status</div>', unsafe_allow_html=True)
    today_supps = [s for s in load("supplement") if s.get("date") == today]
    sups_list = ["Creatine", "Vitamin D", "Omega 3", "Magnesium", "Zinc"]
    if today_supps:
        ts = today_supps[-1]
        cols_ = st.columns(5)
        for i, s in enumerate(sups_list):
            key = s.lower().replace(" ", "_")
            taken = ts.get(key, False)
            icon = "✅" if taken else "❌"
            cols_[i].markdown(f"<div style='text-align:center'>{icon}<br><small>{s}</small></div>",
                              unsafe_allow_html=True)
    else:
        st.info("No supplement log yet today. Go to 💊 Supplements to log.")

    # Charts
    st.markdown('<div class="section-header">📈 Trends</div>', unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        if not bdf.empty and "bodyweight" in bdf:
            bdf2 = bdf.copy()
            bdf2["date"] = pd.to_datetime(bdf2["date"])
            fig = px.line(bdf2.sort_values("date"), x="date", y="bodyweight",
                          title="⚖️ Bodyweight", color_discrete_sequence=["#6366f1"])
            fig.update_traces(line_width=2.5, mode="lines+markers", marker_size=5)
            fig.update_layout(**CHART_LAYOUT, height=280)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No body data yet.")

    with col_r:
        if not ndf.empty and "protein" in ndf:
            ndf2 = ndf.copy()
            ndf2["date"] = pd.to_datetime(ndf2["date"])
            fig2 = px.bar(ndf2.sort_values("date").tail(14), x="date", y=["calories", "protein"],
                          title="🥗 Nutrition (last 14 days)", barmode="overlay",
                          color_discrete_sequence=["#f87171", "#4ade80"])
            fig2.update_layout(**CHART_LAYOUT, height=280)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No nutrition data yet.")

    # Weekly workout volume
    if not wdf.empty and "volume" in wdf:
        wdf2 = wdf.copy()
        wdf2["date"] = pd.to_datetime(wdf2["date"])
        wdf2["volume"] = pd.to_numeric(wdf2["volume"], errors="coerce")
        weekly = wdf2.groupby(wdf2["date"].dt.isocalendar().week)["volume"].sum().reset_index()
        weekly.columns = ["week", "total_volume"]
        fig3 = px.bar(weekly.tail(12), x="week", y="total_volume",
                      title="📦 Weekly Volume (kg lifted)", color_discrete_sequence=["#6366f1"])
        fig3.update_layout(**CHART_LAYOUT, height=260)
        st.plotly_chart(fig3, use_container_width=True)

    # Recovery radar
    if not rdf.empty:
        rdf_last = rdf.iloc[-1]
        cats = ["Sleep", "Stress (inv)", "Energy", "Recovery Score"]
        sleep_norm = min(float(rdf_last.get("sleep_hours", 0)) / 9 * 5, 5)
        stress_inv = 5 - float(rdf_last.get("stress_level", 5))
        energy = float(rdf_last.get("energy_level", 0))
        rhr = rdf_last.get("resting_hr", 60)
        rhr_score = max(0, 5 - (float(rhr) - 50) / 10) if rhr else 2.5

        fig4 = go.Figure(go.Scatterpolar(
            r=[sleep_norm, stress_inv, energy, rhr_score],
            theta=["Sleep Quality", "Low Stress", "Energy", "Heart Health"],
            fill="toself", fillcolor="rgba(99,102,241,0.25)",
            line_color="#6366f1", name="Recovery"
        ))
        fig4.update_layout(**CHART_LAYOUT, height=300, title="🔄 Recovery Radar",
                           polar=dict(bgcolor="#13161f",
                                      radialaxis=dict(visible=True, range=[0, 5], color="#7c8db5"),
                                      angularaxis=dict(color="#7c8db5")))
        st.plotly_chart(fig4, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PAGE: WORKOUT LOG
# ═══════════════════════════════════════════════════════════
elif page == "🏋️ Workout":
    st.markdown('<div class="section-header">🏋️ Log Workout</div>', unsafe_allow_html=True)

    TRAINING_DAYS = ["Upper A", "Upper B", "Lower A", "Lower B", "Push", "Pull", "Legs", "Full Body", "Recovery / Mobility", "Cardio", "Rest"]
    EXERCISES = [
        "Bench Press", "Incline Bench", "OHP", "Dumbbell Press", "Cable Fly", "Chest Dip",
        "Pull-Up", "Barbell Row", "Cable Row", "Lat Pulldown", "Face Pull",
        "Squat", "Romanian Deadlift", "Leg Press", "Leg Curl", "Leg Extension", "Calf Raise",
        "Deadlift", "Hip Thrust", "Plank", "Ab Wheel", "Lateral Raise", "Curl", "Tricep Pushdown",
        "Other"
    ]

    with st.form("workout_form"):
        st.markdown('<div class="form-box">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            w_date    = st.date_input("📅 Date", value=date.today())
            w_day     = st.selectbox("💪 Training Day", TRAINING_DAYS)
        with c2:
            w_ex      = st.selectbox("🏋️ Exercise", EXERCISES)
            w_ex_custom = st.text_input("Or type custom exercise", placeholder="e.g. Nordic Curl")

        c3, c4, c5, c6 = st.columns(4)
        with c3: w_sets   = st.number_input("Sets",   min_value=1, max_value=20, value=3)
        with c4: w_reps   = st.number_input("Reps",   min_value=1, max_value=100, value=10)
        with c5: w_weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, value=60.0, step=2.5)
        with c6:
            volume = round(w_sets * w_reps * w_weight, 1)
            st.metric("📦 Volume", f"{volume} kg")

        w_notes = st.text_area("📝 Notes", placeholder="RPE, fatigue, form cues…", height=80)
        st.markdown('</div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("💾 Save Set")

    if submitted:
        exercise = w_ex_custom.strip() if w_ex_custom.strip() else w_ex
        entry = {
            "date": str(w_date), "training_day": w_day, "exercise": exercise,
            "sets": int(w_sets), "reps": int(w_reps), "weight": float(w_weight),
            "volume": volume, "notes": w_notes
        }
        data = load("workout")
        data.append(entry)
        save("workout", data)

        # Auto-update PR
        prs = load("pr")
        pr_map = {p["exercise"]: p for p in prs}
        if exercise not in pr_map:
            pr_map[exercise] = {"exercise": exercise, "best_weight": w_weight, "best_reps": w_reps, "date": str(w_date)}
        else:
            if w_weight > pr_map[exercise]["best_weight"] or \
               (w_weight == pr_map[exercise]["best_weight"] and w_reps > pr_map[exercise]["best_reps"]):
                pr_map[exercise] = {"exercise": exercise, "best_weight": w_weight, "best_reps": w_reps, "date": str(w_date)}
                st.balloons()
                st.success("🏆 NEW PR! Auto-saved to PR Tracker!")
        save("pr", list(pr_map.values()))
        st.success(f"✅ Saved: {exercise} — {w_sets}×{w_reps} @ {w_weight}kg (Vol: {volume}kg)")

    # History
    st.markdown('<div class="section-header">📋 Workout History</div>', unsafe_allow_html=True)
    wdf = to_df("workout")
    if not wdf.empty:
        # Filter by exercise
        exercises_logged = ["All"] + sorted(wdf["exercise"].unique().tolist())
        sel = st.selectbox("Filter by exercise", exercises_logged)
        df_show = wdf if sel == "All" else wdf[wdf["exercise"] == sel]

        st.dataframe(df_show.sort_values("date", ascending=False).head(50),
                     use_container_width=True, hide_index=True)

        if sel != "All":
            df_plot = df_show.copy()
            df_plot["date"] = pd.to_datetime(df_plot["date"])
            df_plot["weight"] = pd.to_numeric(df_plot["weight"], errors="coerce")
            fig = px.line(df_plot.sort_values("date"), x="date", y="weight",
                          title=f"📈 {sel} — Weight Progression",
                          color_discrete_sequence=["#6366f1"])
            fig.update_traces(mode="lines+markers", line_width=2.5, marker_size=6)
            fig.update_layout(**CHART_LAYOUT, height=300)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No workouts logged yet. Add your first one above!")
