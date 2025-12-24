import streamlit as st
from backend.llm import ask_gemini


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Funding AI",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🇮🇳 Multilingual Funding Intelligence System")
st.caption("AI-powered funding, investor & policy intelligence for founders")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🧠 Features")

feature = st.sidebar.radio(
    "Choose a feature",
    (
        "Eligibility Check",
        "Regional Funding",
        "Funding Trends",
        "Policy Simplifier",
        "Investor Interest",
        "Common Rejection Reasons"
    )
)

st.sidebar.markdown("---")

st.sidebar.header("🌐 Language")
language = st.sidebar.selectbox(
    "Select language",
    ("English", "Malayalam", "Hindi")
)

# ---------------- MAIN AREA ----------------
st.subheader(f"🔍 {feature}")

# ---- FEATURE-SPECIFIC INPUTS ----

# Eligibility Check inputs
if feature == "Eligibility Check":
    col1, col2 = st.columns(2)
    with col1:
        startup_age = st.number_input("Startup age (years)", min_value=0.0, step=0.1)
        sector = st.text_input("Sector (e.g., Agritech, Fintech)")
    with col2:
        revenue_stage = st.selectbox(
            "Revenue stage",
            ("Pre-revenue", "Early revenue", "Growing revenue")
        )
        state = st.text_input("State")

# Regional Funding inputs
elif feature == "Regional Funding":
    state = st.text_input("Enter your state")

# Policy Simplifier inputs
elif feature == "Policy Simplifier":
    uploaded_file = st.file_uploader(
        "Upload policy document (PDF)",
        type=["pdf"]
    )

# Funding Trends / Investor features / Rejection reasons
question = st.text_area(
    "Ask your question",
    placeholder="Type your question here..."
)

submit = st.button("Submit")

# ---------------- DEBUG OUTPUT (TEMPORARY) ----------------
# ---------------- SUBMIT HANDLER ----------------
if submit:
    st.markdown("### 🤖 AI Response")

    # Base prompt (temporary – will become smarter later)
    prompt = f"""
    You are an AI assistant for startup funding and investor intelligence.
    Reply clearly and concisely.

    Language: {language}
    Feature: {feature}

    User Question:
    {question}
    """

    # Call Gemini
    answer = ask_gemini(prompt)

    # Display answer
    st.write(answer)

    # ---- Debug Info (optional, remove later) ----
    with st.expander("🔧 Debug Info"):
        st.write("Selected Feature:", feature)
        st.write("Selected Language:", language)
        st.write("Question:", question)

        if feature == "Eligibility Check":
            st.write({
                "Startup Age": startup_age,
                "Sector": sector,
                "Revenue Stage": revenue_stage,
                "State": state
            })

        if feature == "Policy Simplifier":
            st.write("Uploaded file:", uploaded_file.name if uploaded_file else "No file")
