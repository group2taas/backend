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
