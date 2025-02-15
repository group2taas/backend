from langchain.prompts import PromptTemplate

ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["interview_answers"],
    template="""You are an expert in cybersecurity penetration testing.
Based solely on the interview answers provided and the OWASP guidelines, write a complete Python script that implements multiple tests on the given information.
Your output must contain only the Python code—no explanations, no comments, no extra text.
Do not output any thoughts or analysis, only code.

Interview Answers:
{interview_answers}
"""
)
