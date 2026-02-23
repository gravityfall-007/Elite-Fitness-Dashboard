# 🏋️ ELITE FITNESS OS — Dashboard Setup Guide

## What's Inside
A **mobile-friendly Python dashboard** tracking all 7 systems:
- 🏋️ Workout Log (progressive overload tracking)
- 🏆 PR Tracker (auto-updated when you hit new records)
- 📏 Body Metrics (recomposition tracking)
- 🥗 Nutrition (calories, macros, water)
- 😴 Recovery (sleep, stress, energy, HR)
- 💊 Supplements (daily compliance)
- 🧬 Hormone Health (steps, sunlight, alcohol, training)

All data stored **locally** as JSON files in `fitness_data/`.

---

## ⚡ Quick Start

### Step 1 — Install Python 3.10+
Download from https://python.org if you don't have it.

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the app
```bash
streamlit run app.py
```

Your browser opens automatically at `http://localhost:8501`

---

## 📱 Access from Your Smartphone

1. Find your computer's local IP address:
   - **Windows**: Open CMD → type `ipconfig` → look for `IPv4 Address`
   - **Mac/Linux**: Open Terminal → type `ifconfig` or `ip addr`

2. Make sure your phone is on the **same Wi-Fi** as your computer

3. Open your phone browser and go to:
   ```
   http://192.168.X.X:8501
   ```
   (Replace with your actual IP address)

4. Bookmark it on your home screen for one-tap access!

---

## 🌐 Access Anywhere (Optional)

To access from anywhere (not just home network):

### Option A — ngrok (free, easy)
```bash
pip install pyngrok
ngrok http 8501
```
Use the HTTPS URL it gives you from any device.

### Option B — Streamlit Community Cloud (free hosting)
1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Deploy with one click

---

## 📁 Data Storage
All your data is saved in `fitness_data/`:
```
fitness_data/
├── workouts.json
├── pr_tracker.json
├── body_metrics.json
├── nutrition.json
├── recovery.json
├── supplements.json
└── hormone.json
```
**Back these up** regularly to Google Drive or Dropbox!

---

## 📊 Dashboard Features

| Page | What You Log | Auto-Generated |
|------|-------------|----------------|
| Dashboard | — | Live snapshot of all metrics + charts |
| 🏋️ Workout | Sets, reps, weight, exercise | Volume calc, exercise history |
| 🏆 PRs | — | Auto-updated when new PR hit |
| 📏 Body | Weight, measurements, bodyfat | Lean mass, composition charts |
| 🥗 Nutrition | Calories, macros, water | Macro pie, compliance bars |
| 😴 Recovery | Sleep, stress, energy, HR | Recovery Score (1-5) |
| 💊 Supplements | 5 supplements checklist | Compliance % charts |
| 🧬 Hormones | Steps, sunlight, alcohol, training | Hormone Health Score |

---

## 📅 Daily Use Protocol (5 min/day)

**Every day:**
- Log workout sets in 🏋️ Workout
- Check off supplements in 💊 Supplements
- Enter nutrition in 🥗 Nutrition
- Log recovery before bed in 😴 Recovery

**Weekly:** Check 📏 Body + 🏆 PRs

**Monthly:** Review trends in 📊 Dashboard

---

## 🔧 Customization

Open `app.py` to customize:
- `EXERCISES` list — add your specific exercises
- `TRAINING_DAYS` — change to your program structure
- Target values in Nutrition progress bars
- Supplement names in `SUPPS` list

---

Built with Streamlit + Plotly · Dark theme · Mobile-first design