import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt

# ======================
# LOAD MODEL
# ======================
model = pickle.load(open("model (3).pkl", "rb"))
vectorizer = pickle.load(open("vectorizer (2).pkl", "rb"))

# ======================
# PAGE SETTINGS
# ======================
st.set_page_config(page_title="Smishing Detection", layout="wide")

# ======================
# CUSTOM CSS (KEEP SAME THEME)
# ======================
st.markdown("""
<style>
.stApp { background-color: black; color: white; }

h1, h2, h3 { color: #ff4da6; }

textarea {
    background-color: #111 !important;
    color: white !important;
}

.stButton button {
    background-color: #ff4da6;
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# TITLE
# ======================
st.title("📱 Smishing Detection System")
st.write("Detect fraudulent SMS messages using Machine Learning")

# ======================
# LAYOUT
# ======================
col1, col2 = st.columns([3,1])

# ======================
# LEFT PANEL
# ======================
with col1:
    sms = st.text_area("✉️ Enter SMS Message")

    if st.button("🔍 Analyze Message"):

        if sms.strip() == "":
            st.warning("Please enter a message")

        else:
            data = vectorizer.transform([sms])
            prediction = model.predict(data)[0]
            prob = model.predict_proba(data)[0]

            spam_prob = prob[1]
            safe_prob = prob[0]

            st.subheader("📊 Result")

            if prediction == 1:
                st.error(f"🚨 SPAM MESSAGE ({spam_prob*100:.2f}%)")
            else:
                st.success(f"✅ SAFE MESSAGE ({safe_prob*100:.2f}%)")

            # ======================
            # PROGRESS BAR
            # ======================
            st.subheader("📈 Spam Probability")
            st.progress(int(spam_prob * 100))

            # ======================
            # BAR GRAPH (NEW)
            # ======================
            st.subheader("📊 Probability Distribution")

            fig, ax = plt.subplots()
            labels = ['Safe', 'Spam']
            values = [safe_prob, spam_prob]

            ax.bar(labels, values)
            ax.set_ylim([0,1])
            ax.set_ylabel("Probability")

            st.pyplot(fig)

            # ======================
            # MESSAGE ANALYSIS
            # ======================
            st.subheader("📋 Message Analysis")

            word_count = len(sms.split())
            char_count = len(sms)

            st.write(f"Words: {word_count}")
            st.write(f"Characters: {char_count}")

            # ======================
            # RISK LEVEL
            # ======================
            st.subheader("⚠️ Risk Level")

            if spam_prob > 0.75:
                st.error("HIGH RISK 🚨")
            elif spam_prob > 0.4:
                st.warning("MEDIUM RISK ⚠️")
            else:
                st.success("LOW RISK ✅")

            # ======================
            # KEYWORD DETECTION
            # ======================
            st.subheader("🔍 Detected Keywords")

            spam_keywords = [
                "click","money","win","free","offer",
                "link","urgent","reward","verify","account"
            ]

            found = False
            for word in sms.split():
                if word.lower() in spam_keywords:
                    st.markdown(f"🔴 **{word}**")
                    found = True

            if not found:
                st.write("No suspicious keywords found")

# ======================
# RIGHT PANEL
# ======================
with col2:
    st.sidebar.title("📊 Info Panel")

    st.sidebar.write("Model: Logistic Regression")
    st.sidebar.write("Accuracy: ~93%")
    st.sidebar.write("F1 Score: ~94%")

    st.sidebar.markdown("---")

    st.sidebar.subheader("🧪 Try Examples")

    if st.sidebar.button("Spam Example"):
        st.session_state.sms = "click this link and get money"

    if st.sidebar.button("Normal Example"):
        st.session_state.sms = "hey kese ho"

    st.sidebar.markdown("---")
    st.sidebar.write("Smishing Detection Project")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("💡 Built with Machine Learning + Streamlit")