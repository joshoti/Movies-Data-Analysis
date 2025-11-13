from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_ollama import OllamaLLM

from api.v2.common import OLLAMA_BASE_URL, OLLAMA_MODEL

db = SQLDatabase.from_uri("sqlite:///instance/movies.db")
llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

agent_executor = create_sql_agent(
    llm, db=db, agent_type="zero-shot-react-description", verbose=True
)


class RAGService:
    def answer_question(self, prompt: str):
        return agent_executor.run(prompt)


rag_service = RAGService()
