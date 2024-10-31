from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

loader = TextLoader('./poker.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=4)
docs = text_splitter.split_documents(documents)


embeddings = HuggingFaceEmbeddings()

import os
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from pinecone import ServerlessSpec

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "langchain-demo"
checker = True
indexes = pc.list_indexes()
for index in indexes:
    if index_name == index.name:
       docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
       checker=False 
       break

if checker:    
    pc.create_index(name=index_name, metric="cosine", dimension=768, spec=ServerlessSpec(cloud='aws', region='us-east-1'))
    docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)


from langchain.llms import HuggingFaceHub

# Define the repo ID and connect to Mixtral model on Huggingface
repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(
  repo_id=repo_id, 
  model_kwargs={"temperature": 0.8, "top_k": 50}, 
  huggingfacehub_api_token=os.getenv('HUGGING_FACE_API_KEY')
)

from langchain import PromptTemplate

template = """
You are a poker expert. These Human will ask you a questions about poker strategy. 
Use following piece of context to answer the question. 
If you don't know the answer, just say you don't know. 
Keep the answer within 2 sentences and concise. Use examples to explain where applicable.

Context: {context}
Question: {question}
Answer: 

"""

prompt = PromptTemplate(
  template=template, 
  input_variables=["context", "question"]
)

from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

rag_chain = (
  {"context": docsearch.as_retriever(),  "question": RunnablePassthrough()} 
  | prompt 
  | llm
  | StrOutputParser() 
)

class ChatBot():
  loader = TextLoader('./poker.txt')
  documents = loader.load()

  # The rest of the code here

  rag_chain = (
    {"context": docsearch.as_retriever(),  "question": RunnablePassthrough()} 
    | prompt 
    | llm
    | StrOutputParser() 
  )
  
  # Outside ChatBot() class
bot = ChatBot()
inp = input("Ask me anything: ")
result = bot.rag_chain.invoke(inp)
print(result)