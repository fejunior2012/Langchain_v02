from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

_ = load_dotenv()

# 1. Carrega o nosson conjunto de dados através do CSVLoader
loader = CSVLoader(file_path="knowledge_base.csv")
documents = loader.load()

# Embeddings e vetorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# Modelo de linguagem
llm = ChatOpenAI()

# RAG - Definição do template e chain
rag_template = """
Você é um atendente de uma empresa. Seu trabalho é conversar com os clientes de uma forma educada, consultando a base de conhecimento da empresa e responder as perguntas de forma simples.

Contexto: {context}

Pergunta do cliente: {question}
"""


prompt = ChatPromptTemplate.from_template(rag_template)
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
     | prompt
     | llm
)

# Remova o codigo abaixo para executar o servidor.py
# Pergunta e resposta
print("Sugestão: Pergunte qual o ano de descobrimento do Brasil?")
while True:
    user_input = input("Eu: ")
    response = chain.invoke(user_input)
    print(response.content)
