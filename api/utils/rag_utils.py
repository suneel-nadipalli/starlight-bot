from numpy import dot
from numpy.linalg import norm

import os, sys, json

import urllib.request

from dotenv import load_dotenv

load_dotenv()

sys.path.append("..")

def clean_doc(doc):
    doc = doc.replace("\n", " ")

    doc = doc.replace("\t", " ")

    doc = doc.replace("  ", " ")

    doc = ' '.join(doc.split())

    doc = doc[:5000]

    return doc

class Source:

    def __init__(self, content, embedding, source, similarity):
        
        self.content = clean_doc(content)
        self.embedding = embedding
        self.source = source
        self.similarity = similarity
    
    def __str__(self):
        return f"Source: {self.source}, Similarity: {self.similarity}"
    
    def calculate_similarity(self, query_embedding):
        
        self.similarity = dot(query_embedding, self.embedding)/(norm(query_embedding)*norm(self.embedding))

        self.similarity = round(self.similarity, 3)

        self.embedding = 0
        
def az_rag_query(query, history):

    prompt =  f"""
            Use the following context, presented in the format of a Python list containing the previous
            question-answer pairs in a dictionary, to answer the next question provided by the user:

            context: {history}

            question: {query}

            """ 
    
    data = {"query":f"{prompt}"}

    body = str.encode(json.dumps(data))

    url = os.getenv('AZURE_PF_URL')

    api_key = os.getenv('AZURE_PF_API_KEY')

    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")


    headers = {'Content-Type':'application/json', 
               'Authorization':('Bearer '+ api_key), 
               'azureml-model-deployment': f'suneel-8009-zquye-1'}
    
    req = urllib.request.Request(url, body, headers)

    try:
        
        response = urllib.request.urlopen(req)

        result = response.read()
        
        result_json = json.loads(result.decode('utf-8'))
        
        answer = result_json['reply']

    except urllib.error.HTTPError as error:
        
        print("The request failed with status code: " + str(error.code))
        
        print(error.info())
        
        print(error.read().decode("utf8", 'ignore')) 

    history.append(
        {
            "query": query,
            "reply": answer
        }
    )

    return answer, history
