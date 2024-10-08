# Importing required libraries

from langchain.chat_models import ChatOpenAI

from langchain.memory import ConversationBufferMemory

from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader

from langchain_community.document_loaders.merge import MergedDataLoader

from langchain.chains import ConversationChain

from dotenv import load_dotenv

from glob import glob

import os

# loading in environtment variables from .env file
load_dotenv(dotenv_path="./.env.local")

# setting OPENAI_API_KEY to the environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def get_urls(file):

    with open(file) as file:
        urls = [line.rstrip() for line in file]
    
    return urls

def get_data(dir):

    loaders = []

    for file in glob(f"{dir}/*"):
        if file.endswith(".pdf"):
        
            loader = PyPDFLoader(file)
            loaders.append(loader)
            
        elif file.endswith(".txt"):

            if "urls" in file:

                urls = get_urls(file)
                loader = WebBaseLoader(urls)
                loaders.append(loader)
            else:
                loader = TextLoader(file)
                loaders.append(loader)
    
    merged_loader = MergedDataLoader(loaders=loaders)
        
    return merged_loader.load()

def init_llm():

    """
    Initializes the language model
        
        Parameters:
            None
        
        Returns:
            original_chain (ConversationChain): The language model chain initialized on GPT-4
    """

    # Initializing the language model with GPT-4 
    llm = ChatOpenAI(temperature=0, model_name='gpt-4')
    
    # Initializing the language model chain with the language model and memory
    original_chain = ConversationChain(
        llm=llm,
        memory=ConversationBufferMemory()
    )

    return original_chain

def query_llm(query, chain):

    """
    Queries the language model with a user query and returns the response

        Parameters:
            query (str): The user query
            chain (ConversationChain): The language model chain
        
        Returns:
            response (str): The response from the language model
    """

    # If the chain is not initialized, initialize it
    if not chain:
        chain = init_llm()

    # Querying the language model with the user query
    response = chain.run(query) 

    return response