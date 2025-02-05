from langchain.prompts import PromptTemplate

TECHNICAL_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["analysis", "recommendations", "client_type"],
    template="""You are an AI assistant that has extensive experience in cybersecurity penetration testing.
Your task is to analyse the input derived from scoping questions to generate an exhaustive list of test cases
according to the OWASP framework.

Your output must strictly return a valid JSON
No code blocks, no extra words, no explanations. 
The JSON should follow the format of:
{{
    {
        <testcase 1>: <duration>,
        <testcase 2>: <duration>,
        ...
    }...
}}

Given are the inputs from the scoping questions:
Tech Stack: {tech_stack}
Security Concerns: {security_concerns}
Client Type: {client_type}
"""
)

# TECHNICAL_ANALYSIS_PROMPT = PromptTemplate(
#     input_variables=["tech_stack", "security_concerns", "client_type"],
#     template="""You are an AI assistant that provides a technical analysis. 
# Your output must be valid JSON nothing else.
# No code blocks, no extra words. 
# The JSON should have the following structure:
# {{
#     "analysis": "...",
#     "recommendations": [...]
# }}

# Tech Stack: {tech_stack}
# Security Concerns: {security_concerns}
# Client Type: {client_type}"""
# )

