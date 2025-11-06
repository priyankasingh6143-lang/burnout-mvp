
import re
import pandas as pd
import numpy as np
from datetime import datetime

NEG_WORDS = {
    "overwhelmed","burned","burnt","burnout","exhausted","tired","fatigued","stressed","anxious",
    "pressure","toxic","unfair","ignored","micromanaged","late","overwork","overworked","cry","breakdown",
    "panic","panic attack","dread","hopeless","helpless","no growth","no future","quit","quitting","resign"
}

POS_WORDS = {"supported","recognized","appreciated","balanced","encouraged","fair","growth","autonomy","trust"}

def simple_sentiment(text: str) -> float:
    """Return a simple sentiment score in [-1, 1] based on presence of words."""
    if not text:
        return 0.0
    t = text.lower()
    neg = sum(1 for w in NEG_WORDS if w in t)
    pos = sum(1 for w in POS_WORDS if w in t)
    score = (pos - neg) / max(1, (pos + neg))
    # clamp
    if score > 1: score = 1.0
    if score < -1: score = -1.0
    return float(score)

def burnout_flag(q_scores, sentiment_score):
    """
    Heuristic:
      - average of q1..q4 on 1-5 scale; higher = worse (assume 1=Never, 5=Very Often for strain items)
      - flag if avg >= 3.5 OR sentiment <= -0.4
    """
    if not q_scores:
        return 0
    avg = np.mean(q_scores)
    return int((avg >= 3.5) or (sentiment_score <= -0.4))

PII_PATTERNS = [
    re.compile(r'[A-Za-z0-9\._%+-]+@[A-Za-z0-9\.-]+\.[A-Za-z]{2,}'),  # emails
    re.compile(r'\+?\d[\d\-\s]{7,}\d'),  # phone-like
    re.compile(r'@[A-Za-z0-9_]+'),  # @handles
]

def redact_pii(text: str) -> str:
    if not text:
        return ""
    redacted = str(text)
    for pat in PII_PATTERNS:
        redacted = pat.sub('[REDACTED]', redacted)
    # crude name redaction for capitalized First Last patterns (optional light pass)
    redacted = re.sub(r'\b([A-Z][a-z]+)\s([A-Z][a-z]+)\b', r'\1 [REDACTED]', redacted)
    return redacted

def today_iso():
    return datetime.utcnow().strftime('%Y-%m-%d')
