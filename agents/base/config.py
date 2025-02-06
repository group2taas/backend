from langchain_core.prompts import ChatPromptTemplate

OWASP_CHECKLIST_FILEPATH = "cleaned_owasp_checklist.xlsx"
OWASP_TEMPLATE = """
    Use the following pieces of retrieved context on OWASP Application 
    Security Verification standards, write some python code based on 
    the user's question. Return only python code in Markdown format, e.g.:

    ```python
    ....
    ```
    """
OWASP_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", OWASP_TEMPLATE),
        (
            "human",
            "\Question: {question}\nContext: {context}\nAnswer:",
        ),
    ]
)
