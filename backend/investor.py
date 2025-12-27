from backend.llm import ask_gemini


def investor_interest(
    sector: str,
    revenue_stage: str,
    state: str,
    language: str
) -> str:
    prompt = f"""
    You are an AI startup investment analyst.

    Respond in this language: {language}

    STARTUP PROFILE:
    - Sector: {sector}
    - Revenue stage: {revenue_stage}
    - Location: {state}

    TASK:
    Explain what investors typically look for in startups like this.
    Cover:
    - Key metrics
    - Traction expectations
    - Team & product signals
    - tables for better representation of data if any 

    Be concise, practical, and founder-friendly.
    """

    return ask_gemini(prompt)


def rejection_reasons(
    sector: str,
    revenue_stage: str,
    state: str,
    language: str
) -> str:
    prompt = f"""
    You are an AI venture capital analyst.

    Respond in this language: {language}

    STARTUP PROFILE:
    - Sector: {sector}
    - Revenue stage: {revenue_stage}
    - Location: {state}

    TASK:
    List the most common reasons startups like this get rejected by investors.
    Also suggest how founders can avoid these mistakes.

    Be constructive, honest, and practical.
    and not toooo lengthy, keep it optimized 
    """

    return ask_gemini(prompt)
