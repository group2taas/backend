import os
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_experimental.utilities import PythonREPL
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredExcelLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from loguru import logger
from dotenv import load_dotenv
from IPython.display import display, Markdown
from config import OWASP_CHECKLIST_FILEPATH, OWASP_TEMPLATE, OWASP_PROMPT


load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class OWASPModelHandler:
    def __init__(self, reference: str = OWASP_CHECKLIST_FILEPATH):
        self.llm = self.get_ai_model()
        self.template = OWASP_TEMPLATE
        self.prompt = OWASP_PROMPT
        self.retriever = None
        self.reference = reference

    def get_ai_model(self):
        return ChatOpenAI(
            model="gpt-4o",
            api_key=OPENAI_API_KEY,
            temperature=1,
            max_completion_tokens=None,
            timeout=None,
            max_retries=2,
        )

    def load_owasp_retriever(self, reference: str):
        if reference.endswith("xlsx"):
            logger.info("Using excel loader")
            loader = UnstructuredExcelLoader(reference)
        else:
            logger.info("Using web loader")
            loader = WebBaseLoader(reference)
        try:
            document = loader.load()
            text_splitter = RecursiveCharacterTextSplitter()
            document_chunks = text_splitter.split_documents(document)
            logger.info(OPENAI_API_KEY)
            vector_store = Chroma.from_documents(
                document_chunks, OpenAIEmbeddings(api_key=OPENAI_API_KEY)
            )
            retriever = vector_store.as_retriever()
            return retriever
        except Exception as e:
            logger.error(f"Failed to load from {reference} \n {e}")

    def create_rag_chain(self):
        if self.retriever is None:
            logger.warning("Please create a retriever first. Quitting...")
            return
        try:
            rag_chain = (
                {"context": self.retriever, "question": RunnablePassthrough()}
                | self.prompt
                | self.llm
                | StrOutputParser()
            )
            logger.info(f"RAG chain created: {rag_chain}")
            return rag_chain
        except Exception as e:
            logger.error(f"Failed to create an agent. \n {e}")

    def create_agent(self):
        _, ext = os.path.splitext(self.reference)
        if ext == ".csv":
            df = pd.read_csv(self.reference)
        elif ext == ".json":
            df = pd.read_json(self.reference)
        elif ext in {".xls", ".xlsx"}:
            df = pd.read_excel(self.reference)
        else:
            raise ValueError("Reference type is not currently supported")
        try:
            agent = create_pandas_dataframe_agent(
                llm=self.llm,
                df=df,
                verbose=True,
                suffix=self.template,
                allow_dangerous_code=True,
                include_df_in_prompt=None,
                agent_type=AgentType.OPENAI_FUNCTIONS,
            )
            return agent
        except Exception as e:
            logger.error(
                f"Failed to create agent from given file {self.reference} \n {e}"
            )

    def _sanitize_output(self, text: str):
        _, after = text.split("```python")
        return after.split("```")[0]

    def run_code(self, response: str):
        # TODO: include exception catching and handling
        logger.warning("Successful code execution is not guaranteed...")
        code = self._sanitize_output(response)
        python_repl = PythonREPL()
        python_repl.run(code)

    def display_code(self, response: str):
        display(Markdown(f"{response}"))

    def query_model(self, user_input: str, use_retreiver: bool = True):
        if use_retreiver:
            self.retriever = self.load_owasp_retriever(self.reference)
            rag_chain = self.create_rag_chain()
            response = rag_chain.invoke(user_input)
        else:
            agent = self.create_agent()
            response = agent.invoke(user_input)
            response = response["output"]
        return response
