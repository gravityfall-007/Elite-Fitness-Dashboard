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
