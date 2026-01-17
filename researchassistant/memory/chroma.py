from langchain_openai import  OpenAIEmbeddings
from langgraph.graph import END
from langchain_community.vectorstores import Chroma

embeddings = OpenAIEmbeddings()

vectorstore = Chroma(
    collection_name="user_facts",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

conversation_store = Chroma(
    collection_name="conversation_history",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)