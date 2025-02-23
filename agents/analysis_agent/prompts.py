from langchain.prompts import PromptTemplate

def py_to_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    return f"```python\n{code}\n```"

ZAP_TEMPLATE_SCRIPT = py_to_markdown("template.py")

ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["interview_answers"],
    template=f"""You are an expert in cybersecurity penetration testing.
Based solely on the interview answers provided and the OWASP guidelines, write a complete pentration testing script in Python that implements multiple comprehensive test cases using Selenium and ZAP API.
Your output must be in the following format strictly. Replace <target_url> with the given application url and add relevant test functions.

{ZAP_TEMPLATE_SCRIPT} 

Interview Answers:
{{interview_answers}}
"""
)
