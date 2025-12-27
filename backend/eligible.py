from backend.llm import ask_gemini


def check_eligibility(
    question: str,
    startup_age: float,
    sector: str,
    revenue_stage: str,
    state: str,
    language: str
) -> str:
    """
    Eligibility reasoning with intelligent fallback
    """

    prompt = f"""
    You are an AI startup funding advisor.

    Respond in this language: {language}

    STARTUP PROFILE:
    - Startup age: {startup_age} years
    - Sector: {sector}
    - Revenue stage: {revenue_stage}
    - State: {state}

    USER QUESTION:
    {question}

    TASK:
    1. Assess funding eligibility based on known Indian startup funding practices.
    2. If exact policy rules are available, apply them.
    3. If policy details are partial or unavailable, use informed reasoning
       based on common eligibility patterns (startup age, sector, stage, geography).
    4. Clearly explain your reasoning.
    5. Suggest next steps or alternative funding options.
    6. keep the response concise and optimzed rather than overly lengthy.
    7. could include tables if any, for a better representation of the data.

    IMPORTANT:
    - Do NOT refuse to answer.
    - Avoid saying "I don't have enough information".
    - Be transparent when using general insights.
    - Be practical and founder-friendly.

    Output format:
    - Eligibility Assessment
    - Reasoning
    - Recommendations
    """

    return ask_gemini(prompt)
