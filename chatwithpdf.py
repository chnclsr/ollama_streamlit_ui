from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from Global import *
import streamlit as st
from dataclasses import dataclass

@dataclass
class Message:
    actor: str
    payload: str

@dataclass
class Message:
    actor: str
    payload: str

USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"

# LLM from Ollama
local_model = "llama3:8b"
llm = ChatOllama(model=local_model)
st.title("Chat with PDF")
file = st.file_uploader("Please select a PDF file.", type="pdf")

# Local PDF file uploads
if file:
    loader = UnstructuredPDFLoader(file_path=f"./pdfs/{file.name}")
    data = loader.load()
    page_content = data[0].page_content




    # Split and chunk
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)

    # Add to vector database
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="nomic-embed-text", show_progress=True),
        collection_name="local-rag"
    )

    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(),
        llm,
        prompt=QUERY_PROMPT
    )

    # RAG prompt
    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )



    if MESSAGES not in st.session_state:
        st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="What would you like to learn about the selected PDF?")]

    msg: Message
    for msg in st.session_state[MESSAGES]:
        st.chat_message(msg.actor).write(msg.payload)

    prompt: str = st.chat_input("write your message")

    if prompt:
        st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
        st.chat_message(USER).write(prompt)
        response: str = f"{chain.invoke(prompt)}"
        st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
        st.chat_message(ASSISTANT).write(response)
else:
    print("Upload a PDF file")



# while True:
#     print("---" * 50)
#     inp = input("Ask me a question: ")
#     print(chain.invoke(inp))
#     print("---"*50)
#     print("---"*50)
