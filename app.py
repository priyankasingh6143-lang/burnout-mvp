
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils import simple_sentiment, burnout_flag, redact_pii, today_iso

st.set_page_config(page_title="Burnout Early Warning (v1)", layout="centered")

# Paths
DATA_PATH = "data/sample_checkins.csv"

# Ensure data file exists
def ensure_data():
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except Exception:
        df = pd.DataFrame(columns=[
            "date","user_pseudo_id","role","tenure_bucket","team_id",
            "q1","q2","q3","q4","note_text","note_text_redacted",
            "sentiment_score","burnout_flag"
        ])
        df.to_csv(DATA_PATH, index=False)
        return df

df = ensure_data()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home / Check-in", "Team Dashboard", "Tips"])

st.sidebar.markdown("---")
st.sidebar.caption("Aggregation: Team-level only. Analytics render when **n ≥ 5**.")

def write_row(row_dict):
    global df
    df = pd.concat([df, pd.DataFrame([row_dict])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

# Home / Check-in Page
if page == "Home / Check-in":
    st.title("Weekly Check-in (≤ 60 sec)")
    st.caption("Anonymous team-level check-in. No individual leaderboards.")

    col1, col2 = st.columns(2)
    role = col1.selectbox("Your Role", ["Hourly", "Salaried"])
    tenure = col2.selectbox("Tenure", ["<1y", "1-3y", "3y+"])
    team_id = st.text_input("Team Code (letters/numbers)", value="OPS-ALPHA")

    st.markdown("**In the last week, how often did you experience…** (1=Never, 5=Very Often)")
    q1 = st.slider("Feeling emotionally exhausted", 1, 5, 2)
    q2 = st.slider("Trouble unwinding after work", 1, 5, 2)
    q3 = st.slider("Feeling unappreciated", 1, 5, 2)
    q4 = st.slider("Workload strain", 1, 5, 3)

    note = st.text_area("Optional note (no names/emails).", placeholder="e.g., Deadlines piled up; manager helped adjust priorities.")

    if st.button("Submit"):
        note_red = redact_pii(note)
        s = simple_sentiment(note_red)
        flag = burnout_flag([q1,q2,q3,q4], s)
        row = {
            "date": today_iso(),
            "user_pseudo_id": f"user_{np.random.randint(1000,9999)}",
            "role": role,
            "tenure_bucket": tenure,
            "team_id": team_id,
            "q1": q1, "q2": q2, "q3": q3, "q4": q4,
            "note_text": note,
            "note_text_redacted": note_red[:240],  # truncate
            "sentiment_score": s,
            "burnout_flag": flag
        }
        write_row(row)
        st.success("Thanks! Your response has been recorded (aggregated at team level).")
        st.balloons()

    st.markdown("---")
    st.subheader("What we store (v1)")
    st.write("- Anonymous pseudo-ID")
    st.write("- 4 check-in scores + optional note (redacted)")
    st.write("- Simple sentiment score & flag (heuristic)")
    st.caption("Raw check-ins retained for 90 days; weekly aggregates kept for trends.")

# Team Dashboard
elif page == "Team Dashboard":
    st.title("Team Well-Being **(n ≥ 5)**")
    team_id = st.text_input("Team Code", value="OPS-ALPHA")
    dd = df[df["team_id"] == team_id].copy()

    n = len(dd)
    st.metric("Responses (last 90d)", n)

    if n < 5:
        st.warning("Aggregation privacy rule in effect — need **n ≥ 5** to render analytics.")
    else:
        # Aggregate
        dd["avg_q"] = dd[["q1","q2","q3","q4"]].mean(axis=1)
        week = pd.to_datetime(dd["date"]).dt.to_period("W").astype(str)
        dd["week"] = week
        agg = dd.groupby("week", as_index=False).agg(
            mean_q=("avg_q","mean"),
            participation_n=("avg_q","count"),
            alerts=("burnout_flag","sum"),
            mean_sent=("sentiment_score","mean")
        )
        st.subheader("Trend (weekly)")
        st.line_chart(agg.set_index("week")[["mean_q"]])

        colA, colB, colC = st.columns(3)
        colA.metric("Avg strain (last wk)", f"{agg['mean_q'].iloc[-1]:.2f}")
        colB.metric("Participation (last wk)", int(agg['participation_n'].iloc[-1]))
        colC.metric("Flags (last wk)", int(agg['alerts'].iloc[-1]))

        st.subheader("Participation Parity (role × tenure)")
        pivot = dd.pivot_table(index="role", columns="tenure_bucket", values="user_pseudo_id", aggfunc="count").fillna(0).astype(int)
        st.dataframe(pivot)

        st.caption("Fairness spot-check: We aim for similar participation across role/tenure cohorts.")

# Tips Page
else:
    st.title("Tips & Resources (v0)")
    st.write("General suggestions based on common stress/feedback themes.")
    theme = st.selectbox("Pick a theme", ["Workload", "Recognition", "Feedback", "Boundaries"])
    tips = {
        "Workload": [
            "Time-block 60 minutes daily for deep work; batch interrupts.",
            "Ask your manager to clarify priorities and trade-offs."
        ],
        "Recognition": [
            "Share 1 weekly win in your team channel.",
            "Keep a 'done list' to surface progress in 1:1s."
        ],
        "Feedback": [
            "Use SBI: Situation–Behavior–Impact when giving feedback.",
            "Ask for 1 concrete example and a small next step."
        ],
        "Boundaries": [
            "Define a 'shutdown ritual' at end of shift.",
            "Silence notifications during personal time."
        ]
    }
    st.markdown("**Suggestions:**")
    for t in tips[theme]:
        st.write(f"- {t}")
    st.info("These are general suggestions, not medical advice.")
