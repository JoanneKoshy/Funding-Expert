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

# ---------------- SIDEBAR : LANGUAGE ----------------
st.sidebar.header("🌐 Language")
language = st.sidebar.selectbox(
    "Select language",
    ("English", "Malayalam", "Hindi")
)

# 🔥 UI TEXT MAP
T = UI_TEXT[language]

# ---------------- TITLE ----------------
st.title(T["title"])
st.caption(T["caption"])

# ---------------- SIDEBAR ----------------
st.sidebar.header(T["features"])

feature = st.sidebar.radio(
    T["choose_feature"],
    (
        "Eligibility Check",
        "Regional Funding",
        "Funding Trends",
        "Policy Simplifier",
        "Investor Interest",
        "Common Rejection Reasons"
    ),
    format_func=lambda x: {
        "Eligibility Check": T["eligibility"],
        "Regional Funding": T["regional"],
        "Funding Trends": T["trends"],
        "Policy Simplifier": T["policy"],
        "Investor Interest": T["investor"],
        "Common Rejection Reasons": T["rejection"]
    }[x]
)

st.sidebar.markdown("---")

# ---------------- MAIN AREA (🔥 FIXED FEATURE TITLE) ----------------
feature_label = {
    "Eligibility Check": T["eligibility"],
    "Regional Funding": T["regional"],
    "Funding Trends": T["trends"],
    "Policy Simplifier": T["policy"],
    "Investor Interest": T["investor"],
    "Common Rejection Reasons": T["rejection"]
}[feature]

st.subheader(f"🔍 {feature_label}")


# ---------------- FEATURE INPUTS ----------------

# 🔹 Eligibility
if feature == "Eligibility Check":
    col1, col2 = st.columns(2)
    with col1:
        startup_age = st.number_input(
            T["startup_age"],
            min_value=0.0,
            step=0.1
        )
        sector = st.text_input(T["sector"])
    with col2:
        revenue_stage = st.selectbox(
            T["revenue_stage"],
            ("pre_revenue", "early_revenue", "growing_revenue"),
            format_func=lambda x: T[x]
        )
        state = st.text_input(T["state"])

# 🔹 Regional Funding
elif feature == "Regional Funding":
    state = st.text_input(T["state"])

# 🔹 Investor Inputs
elif feature in ["Investor Interest", "Common Rejection Reasons"]:
    col1, col2 = st.columns(2)
    with col1:
        sector = st.text_input(T["sector"])
        state = st.text_input(T["state"])
    with col2:
        revenue_stage = st.selectbox(
            T["revenue_stage"],
            ("pre_revenue", "early_revenue", "growing_revenue"),
            format_func=lambda x: T[x]
        )

# 🔹 Policy Simplifier
elif feature == "Policy Simplifier":
    uploaded_file = st.file_uploader(
        T["upload_policy"],
        type=["pdf"]
    )

# ---------------- QUESTION BOX ----------------
if feature not in ["Investor Interest", "Common Rejection Reasons"]:
    question = st.text_area(T["ask_question"])
else:
    question = ""

submit = st.button(T["submit"])

# ================= SUBMIT HANDLER =================
if submit:
    st.markdown(f"### {T['thinking']}")

    # 🔥 POLICY SIMPLIFIER
    if feature == "Policy Simplifier":
        if not uploaded_file:
            st.warning(T["upload_policy"])
            st.stop()

        answer = simplify_policy(uploaded_file, question)
        st.write(answer)
        st.stop()

    # 🔥 ELIGIBILITY CHECK
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

    # 🔥 FUNDING TRENDS
    if feature == "Funding Trends":
        normalized_question = translate_to_english(question, language)
        answer = get_funding_trends(normalized_question)
        final_answer = translate_from_english(answer, language)
        st.write(final_answer)
        st.stop()

    # 🔹 REGIONAL FUNDING
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
