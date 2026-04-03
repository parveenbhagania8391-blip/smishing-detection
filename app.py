import streamlit as st
import pickle
import re

# =========================
# Load Model + Vectorizer
# =========================
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# =========================
# Custom CSS (BLACK + PINK THEME)
# =========================
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    h1, h2, h3 { color: white; }

    .stButton>button {
        background-color: #ff4b8b;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }

    .stTextArea textarea {
        background-color: #1c1f26;
        color: white;
    }

    .box {
        padding: 15px;
        border-radius: 10px;
        background-color: #1c1f26;
        margin-bottom: 10px;
    }

    .highlight {
        color: #ff4b8b;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# Text Cleaning
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

# =========================
# Keyword Detection
# =========================
suspicious_keywords = [
    "otp", "urgent", "click", "win", "prize",
    "bank", "verify", "link", "free", "offer",
    "account", "suspend", "update", "reward"
]

def find_keywords(text):
    return [word for word in suspicious_keywords if word in text.lower()]

# =========================
# Highlight Keywords
# =========================
def highlight_text(text, keywords):
    for word in keywords:
        text = re.sub(f"({word})", r"<span class='highlight'>\1</span>", text, flags=re.IGNORECASE)
    return text

# =========================
# UI
# =========================
st.title("📩 Smishing Detection Dashboard")

col1, col2 = st.columns([2,1])

# LEFT PANEL
with col1:
    st.markdown("### 📥 Enter SMS")
    input_text = st.text_area("Type message here...")

    if st.button("Analyze Message"):
        cleaned = clean_text(input_text)
        data = vectorizer.transform([cleaned])

        prediction = model.predict(data)
        prob = model.predict_proba(data)[0][1] * 100  # spam probability %

        keywords = find_keywords(input_text)
        highlighted = highlight_text(input_text, keywords)

        # RESULT BOX
        st.markdown('<div class="box">', unsafe_allow_html=True)

        if prediction[0] == 1:
            st.error("🚨 SMISHING DETECTED")
        else:
            st.success("✅ SAFE MESSAGE")

        st.write(f"### 🎯 Spam Probability: {prob:.2f}%")

        # Risk Meter
        if prob > 75:
            st.error("🔴 HIGH RISK")
        elif prob > 40:
            st.warning("🟠 MEDIUM RISK")
        else:
            st.success("🟢 LOW RISK")

        st.markdown('</div>', unsafe_allow_html=True)

        # Highlighted Message
        st.markdown("### 🔍 Message Analysis")
        st.markdown(f"<div class='box'>{highlighted}</div>", unsafe_allow_html=True)

# RIGHT PANEL
with col2:
    st.markdown("### ⚠️ Detected Keywords")

    if 'input_text' in locals():
        keywords = find_keywords(input_text)

        if keywords:
            for k in keywords:
                st.markdown(f"<div class='box'>🔍 {k}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='box'>No suspicious keywords</div>", unsafe_allow_html=True)