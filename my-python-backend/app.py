from flask import Flask, jsonify, request
from flask_cors import CORS  # For handling CORS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize your chatbot logic here
loader = TextLoader('./poker.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=4)
docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings()

# Pinecone initialization
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "langchain-demo"
checker = True
indexes = pc.list_indexes()
for index in indexes:
    if index_name == index.name:
        docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
        checker = False
        break

if checker:
    pc.create_index(name=index_name, metric="cosine", dimension=768, spec=ServerlessSpec(cloud='aws', region='us-east-1'))
    docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

# Define the model
repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(
    repo_id=repo_id,
    model_kwargs={"temperature": 0.8, "top_k": 50},
    huggingfacehub_api_token=os.getenv('HUGGING_FACE_API_KEY')
)

template = """
You are a poker expert. These Human will ask you a questions about poker strategy. 
Use following piece of context to answer the question. 
If you don't know the answer, just say you don't know. 
Keep the answer within 2 sentences and concise. Use examples to explain where applicable.

Context: {context}
Question: {question}
Answer: 
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

rag_chain = (
    {"context": docsearch.as_retriever(), "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

class ChatBot:
    def __init__(self):
        self.rag_chain = rag_chain

bot = ChatBot()

@app.route('/api/message', methods=['POST'])
def get_message():
    data = request.json
    user_message = data.get('message', '')
    result = bot.rag_chain.invoke(user_message)
    
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True)
