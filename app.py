import streamlit as st

# -------- BACKEND IMPORTS --------
from backend.llm import ask_gemini
from backend.language import translate_to_english, translate_from_english
from backend.rag import retrieve_context_by_state, answer_with_rag
from backend.eligible import check_eligibility
from backend.investor import investor_interest, rejection_reasons
from backend.policy import simplify_policy
from backend.trends import get_funding_trends
from backend.ui_text import UI_TEXT


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Funding AI",
    layout="wide"
)

# ---------------- TITLE ----------------

st.title(" Multilingual Funding Intelligence System")
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

# ---------------- FEATURE INPUTS ----------------

# 🔹 Eligibility
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

# 🔹 Regional Funding
elif feature == "Regional Funding":
    state = st.text_input("Enter your state")

# 🔹 Investor Inputs
elif feature in ["Investor Interest", "Common Rejection Reasons"]:
    col1, col2 = st.columns(2)
    with col1:
        sector = st.text_input("Sector")
        state = st.text_input("State")
    with col2:
        revenue_stage = st.selectbox(
            "Revenue stage",
            ("Pre-revenue", "Early revenue", "Growing revenue")
        )

# 🔹 Policy Simplifier
elif feature == "Policy Simplifier":
    uploaded_file = st.file_uploader("Upload policy document (PDF)", type=["pdf"])

# ---------------- QUESTION BOX ----------------
if feature not in ["Investor Interest", "Common Rejection Reasons"]:
    question = st.text_area("Ask your question")
else:
    question = ""

submit = st.button("Submit")

# ================= SUBMIT HANDLER =================
if submit:
    st.markdown("### Expert is thinking...")

    # 🔥 POLICY SIMPLIFIER (PER-UPLOAD RAG)
    if feature == "Policy Simplifier":
        if not uploaded_file:
            st.warning("Please upload a policy PDF.")
            st.stop()

        answer = simplify_policy(uploaded_file, question)
        st.write(answer)
        st.stop()

    # 🔥 ELIGIBILITY CHECK (PURE REASONING)
    if feature == "Eligibility Check":
        answer = check_eligibility(
            question=question,
            startup_age=startup_age,
            sector=sector,
            revenue_stage=revenue_stage,
            state=state,
            language=language
        )
        st.write(answer)
        st.stop()

    # 🔥 INVESTOR INTEREST
    if feature == "Investor Interest":
        answer = investor_interest(
            sector=sector,
            revenue_stage=revenue_stage,
            state=state,
            language=language
        )
        st.write(answer)
        st.stop()

    # 🔥 COMMON REJECTION REASONS
    if feature == "Common Rejection Reasons":
        answer = rejection_reasons(
            sector=sector,
            revenue_stage=revenue_stage,
            state=state,
            language=language
        )
        st.write(answer)
        st.stop()

    # 🔥 FUNDING TRENDS (HYBRID RAG + LLM)
    if feature == "Funding Trends":
        normalized_question = translate_to_english(question, language)
        answer = get_funding_trends(normalized_question)
        final_answer = translate_from_english(answer, language)
        st.write(final_answer)
        st.stop()

    # 🔹 REGIONAL FUNDING (STATE-AWARE RAG + FALLBACK)
    normalized_question = translate_to_english(question, language)

    if feature == "Regional Funding":
        context = retrieve_context_by_state(normalized_question, state)

        prompt = f"""
You are an AI assistant for regional startup funding intelligence.

Use the provided context as the primary reference.
If the context is incomplete, apply informed reasoning.
Do NOT refuse to answer.

CONTEXT:
{context}

QUESTION:
{normalized_question}
"""
        english_answer = ask_gemini(prompt)

    else:
        english_answer = answer_with_rag(normalized_question)

    final_answer = translate_from_english(english_answer, language)
    st.write(final_answer)

    # ---------------- DEBUG ----------------
    with st.expander("🔧 Debug Info"):
        st.write("Feature:", feature)
        st.write("Language:", language)
        st.write("Question:", question)
