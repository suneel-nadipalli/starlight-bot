from pymongo import MongoClient

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import MongoDBAtlasVectorSearch

from dotenv import load_dotenv

import sys, os, certifi

sys.path.append("..")

from utils import *

load_dotenv(dotenv_path=".env.local")

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

def connect_to_mongo():

    ca = certifi.where()

    client = MongoClient(os.environ.get("MONGO_URI"), tlsCAFile=ca)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client


def insert_data(client=None):
    if not client:
        client = connect_to_mongo()

    data = []
    
    chunks = get_data("../data-src") 

    for chunk in chunks:
        if ".pdf" in chunk.metadata['source']:
            data.append(
                {
                    "text": chunk.page_content,
                    "metadata": {
                        "source": chunk.metadata['source'],
                        "type": "pdf",
                        "page": chunk.metadata['page']
                    }
                }
            )

        elif ".txt" in chunk.metadata['source']:
            data.append(
                {
                    "text": chunk.page_content,
                    "metadata": {
                        "source": chunk.metadata['source'],
                        "type": "txt"
                    }
                }
            )

        elif "https" in chunk.metadata['source']:
            data.append(
                {
                    "text": chunk.page_content,
                    "metadata": {
                        "source": chunk.metadata['source'],
                        "type": "url"
                    }
                }
            )

    data_db = client[os.environ.get("MONGO_DB")]

    data_collection = data_db["starlight-data"]

    data_collection.insert_many(data)

    return list(data_collection.find())


def insert_vs(client=None):

    if not client:
        client = connect_to_mongo()
    
    vs_db = client[os.environ.get("MONGO_DB")]

    vs_collection = vs_db[f"starlight-vs"]

    data = get_data("../data-src")

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"), 
                                disallowed_special=())

    # Create embeddings in atlas vector store
    vector_search = MongoDBAtlasVectorSearch.from_documents( 
                                    documents=data, 
                                    embedding= embeddings, 
                                    collection=vs_collection,)
    
    return vector_search


def get_vs(client=None):
    
    if not client:
        client = connect_to_mongo()
    
    vs_db = client[os.environ.get("MONGO_DB")]

    if "starlight-vs" not in vs_db.list_collection_names():
        
        print("inserting vs")
            
        return insert_vs(client=client)
    
    else:
        print("using existing vs collection")

        sl_vs = vs_db[f"starlight-vs"]

        embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"), 
                                disallowed_special=())

        vector_search =  MongoDBAtlasVectorSearch(sl_vs, embeddings)

        # vector_search = MongoDBAtlasVectorSearch.from_connection_string(
        #     os.environ.get("MONGO_URI"),
        #     os.environ.get("MONGO_DB") + "." + f"starlight-vs",
        #     OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"), 
        #                             disallowed_special=()),
        # )
        
        return vector_search