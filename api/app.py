# Importing required libraries

from flask import Flask, request 

from dotenv import load_dotenv

import os

from flask_cors import CORS

from utils import *

# loading in environtment variables from .env file
load_dotenv(dotenv_path="./.env.local")

# setting DEBUG to true as it's not in deployment
DEBUG = bool(os.environ.get("DEBUG", False))

app = Flask(__name__)

# Wrapping Flask app in CORS object to allow cross-origin requests from frontend
CORS(app)

app.config["DEBUG"] = DEBUG

# Initializing the language model
chain = init_llm()

# Defining routes for API

@app.route("/")
def hello_world():
    return 'Hello, World!'

@app.route("/answer-query", methods=["POST"])
def answer_query():

    """
    Takes in a query from the user and returns a response from the language model

        Parameters:
            message (str): The query from the user

        Returns:
            response (str): The response from the language model
    """  

    # parsing JSON request for user query
    data = request.json

    query = data.get("message")

    # querying the language model with the user query
    response = query_llm(query, chain)

    return {"bot": response}

@app.route("/clear-memory", methods=["POST"])
def clear_memory():

    """
    Clears the memory of the language model

        Parameters:
            None
        
        Returns:
            message (str): A message indicating that the memory has been cleared
    """

    # setting chain to be a global variable to keep track of memory being full or null   
    global chain
    
    # reinitializing the language model to clear memory
    chain = init_llm() 
    
    return {"message": "Memory cleared"}

if __name__ == "__main__":
    
    # running the Flask app on port 5050
    app.run(debug=True, port=5050)