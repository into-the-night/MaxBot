from settings import API_Settings

import google.generativeai as genai
import google.ai.generativelanguage as glm
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import VectorStoreIndex

import os
api_key = API_Settings.API_KEY
os.environ["API_KEY"]=api_key

documents = SimpleDirectoryReader(input_files=["doctors.csv"])
documents = documents.load_data()
embed_model = GeminiEmbedding(model_name="models/embedding-001", api_key=api_key)
Settings.embed_model = embed_model
Settings.llm = Gemini(api_key=api_key, temperature=0.7, model='models/gemini-pro')
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=3)

def get_doc_recs(doctor_type: str, location: str) -> str:
    """ get doctor recommendations ONLY when given BOTH type (speciality) of doctor and location of the user"""

    query = f'Give me all information about a doctor of {doctor_type} in {location}'
    response = query_engine.query(query)
    
    return str(response)


genai.configure(api_key=API_Settings.API_KEY)
model = genai.GenerativeModel('gemini-pro', tools=[get_doc_recs])
chat = model.start_chat(history=[])
chat.send_message(content="You are a healthcare bot designed for recommending doctors and solving patient's queries. Your name is Max. YOU CAN ANSWER GENERAL PATIENT QUERIES. \
    You must converse with the me and gather the following fields (YOU MUST NOT MAKE ASSUMPTIONS) from our conversation: 'the speciality of doctor they should be recommended based on their symptoms (must be a normal speciality)' and 'city in which the doctor should be'. When you have ALL REQUIRED DETAILS, THEN YOU CAN RECOMMEND DOCTORS.")


def handle_chat(message):
    response = chat.send_message(content=message)
    part = response.parts[0]
    part = type(part).to_dict(part)
    try:
        if part["function_call"]:
            if part['function_call']['name'] == 'get_doc_recs':
                doc_type = part['function_call']['args']['doctor_type']
                loc = part['function_call']['args']['location']
                func_resp = glm.Part(function_response=glm.FunctionResponse(name="get_doc_recs", response={"result":get_doc_recs(doc_type, loc)}))
                response = chat.send_message(func_resp)
    except KeyError:
        pass
    return response.text

while True:
    message = str(input("User:"))
    print(handle_chat(message))
    if message == "exit":
        break



