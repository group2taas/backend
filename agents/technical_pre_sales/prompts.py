from langchain.prompts import PromptTemplate

TECHNICAL_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["tech_stack", "security_concerns", "client_type"],
    template="""You are an AI assistant that provides a technical analysis. 
Your output must be valid JSON nothing else.
No code blocks, no extra words. 
The JSON should have the following structure:
{{
    "analysis": "...",
    "recommendations": [...]
}}

Tech Stack: {tech_stack}
Security Concerns: {security_concerns}
Client Type: {client_type}"""
)