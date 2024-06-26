from langchain.chat_models import ChatOpenAI

from langchain.memory import ConversationBufferMemory

from langchain.chains import ConversationChain

from dotenv import load_dotenv

import os

load_dotenv(dotenv_path="./.env.local")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def init_llm():
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-0301')
    
    original_chain = ConversationChain(
        llm=llm,
        memory=ConversationBufferMemory()
    )

    return original_chain

def query_llm(query, chain):
    if not chain:
        chain = init_llm()
    return chain.run(query)