
# Burnout Early Warning (v1) — Streamlit MVP

This is a minimal, privacy-first MVP to support **Milestone 3 — Prototype v1 & Peer Feedback**.

## 🔗 Live Link (after deploy)
- Streamlit Cloud: create a new app pointing to `app.py` on your GitHub repo.  
- Once deployed, paste your link here (e.g., `https://your-name-burnout-mvp.streamlit.app`).

## ▶️ Run Locally
```bash
# 1) Create & activate a virtual env (optional)
python3 -m venv .venv && source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Launch app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## 🧭 App Flow
- **Home / Check-in**: 4-item weekly check-in + optional note (PII redaction); stores to `data/sample_checkins.csv`
- **Team Dashboard**: Aggregated view, **renders only when n ≥ 5** responses (privacy guardrail)
- **Tips**: General suggestions by theme (v0)

## 🔒 Privacy & Data
- Only anonymous pseudo-IDs are saved; no emails or names.  
- Optional open-text is **redacted** for emails/handles/phones and lightly for names, then truncated.  
- **Retention**: keep raw check-ins 90 days (example policy); aggregates may be retained longer for trends.  
- **Secrets**: No credentials required in this demo. For real deployments, keep secrets in environment variables and **never commit** to the repo.

## 📸 Screenshots for Milestone 3
After running locally, take 2 screenshots:
1. **Home / Check-in** (with the Likert sliders visible)
2. **Team Dashboard** with the **n ≥ 5** label and chart visible

## ☁️ Streamlit Cloud Deploy (5–10 min)
1. Push these files to a public GitHub repo.
2. Go to https://share.streamlit.io/ and create an app from your repo.
3. Set the main file to `app.py`.
4. Click **Deploy**. Paste your app URL into your Milestone 3 document.

## 📑 Files
- `app.py` — Streamlit app
- `utils.py` — helpers (PII redaction, simple sentiment, flag heuristic)
- `data/sample_checkins.csv` — seed data so dashboard renders immediately
- `requirements.txt` — dependencies
- `README.md` — this file

## ✅ Milestone 3 Alignment
- **Links**: Provide Streamlit URL + (optional) GitHub repo
- **Features**: Check-in, AI heuristic, dashboard, n ≥ 5 privacy, tips
- **Screens**: Include 2 screenshots
- **Usability**: Use app to run 3 tasks with 5 users and record results
- **Fairness**: Check participation parity across role×tenure in the dashboard
- **Validity**: Track internal consistency or stability over time (collect ≥4 weeks)
- **Action Plan**: Use reviewer feedback and usability notes to prioritize next steps
