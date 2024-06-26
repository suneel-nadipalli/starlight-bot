from flask import Flask, request

from dotenv import load_dotenv

import os

from flask_cors import CORS

from utils import *

load_dotenv(dotenv_path="./.env.local")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

DEBUG = bool(os.environ.get("DEBUG", False))

app = Flask(__name__)

CORS(app)

app.config["DEBUG"] = DEBUG

chain = init_llm()

@app.route("/")
def hello_world():
    return 'Hello, World!'

@app.route("/echo", methods=["POST"])
def echo():

    data = request.json
    
    query = data.get("message")

    return {"bot": f"Query Echos {query}"}

@app.route("/answer-simple", methods=["POST"])
def answer_simple():

    data = request.json

    query = data.get("message")

    response = query_llm(query, chain)

    return {"bot": response}


if __name__ == "__main__":
    app.run(debug=True, port=5050)