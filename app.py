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
