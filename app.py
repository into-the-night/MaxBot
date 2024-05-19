from settings import API_Settings

import google.generativeai as genai
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import VectorStoreIndex


def get_doc_recs(doctor_type: str, location: str) -> str:
    """ get doctor recommendations ONLY when given BOTH type (speciality) of doctor and location of the user"""

    documents = SimpleDirectoryReader(input_files=["doctors.csv"]).load_data()
    embed_model = GeminiEmbedding(model_name="models/embedding-001", api_key=API_Settings.API_KEY)
    Settings.embed_model = embed_model
    Settings.llm = Gemini(api_key=API_Settings.API_KEY, temperature=0.7)
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(response_mode="tree_summarize", similarity_top_k=2)
    
    response = query_engine.query(f'I want a {doctor_type} in {location}')
    
    return str(response)

genai.configure(api_key=API_Settings.API_KEY)
model = genai.GenerativeModel('gemini-pro', tools=[get_doc_recs])
chat = model.start_chat(history=[])
chat.send_message(content="You are a healthcare bot designed for recommending doctors and booking appointments. Your name is Max. \
    You must converse with the me and gather the following fields (YOU MUST NOT MAKE ASSUMPTIONS) from our conversation: 'the speciality of doctor they should be recommended based on their symptoms (must be a normal speciality)' and 'city in which the doctor should be'. When you have ALL REQUIRED DETAILS, THEN YOU CALL THE FUNCTION TO RECOMMEND DOCTORS ")

while True:
    message = str(input())
    if message == "exit":
        break
    response = chat.send_message(content=message)
    print(response.parts)

print(chat.history)
# create_json = model.start_chat(history=chat.history)
# query_json = create_json.send_message(content="Read the conversation above and reply with ONLY the JSON object with the fields: 'Doctor Type' and 'Location'")






