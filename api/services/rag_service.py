import os

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///instance/movies.db")
llm = Ollama(model="llama2", base_url=os.environ.get("OLLAMA_BASE_URL"))

agent_executor = create_sql_agent(
    llm, db=db, agent_type="zero-shot-react-description", verbose=True
)


class RAGService:
    def answer_question(self, prompt: str):
        return agent_executor.run(prompt)


rag_service = RAGService()
