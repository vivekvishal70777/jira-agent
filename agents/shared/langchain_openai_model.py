import csv

from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
file_path = "D:/learning2k25/ML/jira.csv"
documents=[]
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")



def create_embedding_in_vector_store():
    with open(file_path, mode='r',encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for rowid,row in enumerate(reader):
            content = "\n".join([f"{k}: {v}" for k, v in row.items()])
            create_doc = Document(page_content=content,metadata = {"row": rowid})
            documents.append(create_doc)
        print("Created")

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./vector_db"
    )
    print(vector_store)

def retrieve_similar_data_from_vector_store(query):
    read_data_from_chroma = Chroma(
        embedding_function=embeddings,
        persist_directory="./vector_db"
    )
    #query = "Database connection is dropping in database"
    retriever=read_data_from_chroma.similarity_search(query)
    #print(retriever)
    context = "\n".join(doc.page_content for doc in retriever)
    return context

#con=retrieve_similar_data_from_vector_store("Look for the resolution of issue in tool Database connection is dropping in database")
#print(con)

create_embedding_in_vector_store()