# Importing required libraries

from flask import Flask, request 

from dotenv import load_dotenv

from rag_utils import *

import os 

from flask_cors import CORS

# loading in environtment variables from .env file
load_dotenv(dotenv_path="./.env.local")

# setting DEBUG to true as it's not in deployment
DEBUG = bool(os.environ.get("DEBUG", False))

app = Flask(__name__)

# Wrapping Flask app in CORS object to allow cross-origin requests from frontend
CORS(app)

app.config["DEBUG"] = DEBUG

history = []

# Defining routes for API

@app.route("/")
def hello_world():
    return 'Hello, World!'

@app.route("/query_az_rag", methods=["POST"])
def query_az_rag():
    """
    Takes in a query from the user and returns a response from the RAG model

        Parameters:
            message (str): The query from the user

        Returns:
            response (str): The response from the RAG model
    """  

    global history

    # parsing JSON request for user query
    data = request.json

    query = data.get("message")

    answer, history = az_rag_query(query, history)

    response = {
        "answer": answer,
        "srcs": []
    }

    return response


@app.route("/az_clear_memory", methods=["POST"])
def az_clear_memory():

    """
    Clears the memory of the language model

        Parameters:
            None
        
        Returns:
            message (str): A message indicating that the memory has been cleared
    """

    # setting chain to be a global variable to keep track of memory being full or null   
    global history
    
    # reinitializing the language model to clear memory
    history = []
    
    return {"message": "Memory cleared"}


if __name__ == "__main__":
    
    app.run()