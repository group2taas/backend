from langchain.prompts import PromptTemplate

TEST_CASE_GENERATION_PROMPT = PromptTemplate(
    input_variables=["testing_codebase"],
    template="""You are an expert in cybersecurity penetration testing.
Based solely on the generated Python code, come up with a list of test cases that the codebase is testing for.
Your output must contain only a list of generated test cases as a list of strings, separated by commas —no explanations, no comments, no extra text.
Do not output any thoughts or analysis.

Structure your output as follows:
["Test Case 1", "Test Case 2", "Test Case 3", ...]

Interview Answers:
{testing_codebase}
"""
)

PYTHON_SAMPLE_CODE="""
from time import sleep
for i in range(5):
    print(f'{{"target_url": "https://www.instagram.com", "security_alerts": {{"High": 0, "Medium": 13, "Low": 58, "Informational": 42}}, "test_case": "test_case_{i}", "result": "Passed"}}')
    sleep(10)
for i in range(5,10):
    print(f'{{"target_url": "https://www.instagram.com", "security_alerts": {{"High": 0, "Medium": 13, "Low": 58, "Informational": 42}}, "test_case": "test_case_{i}", "result": "Failed"}}')
    sleep(10)
"""