from fastapi import FastAPI, responses, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from request_schemas.chat_schemas import ChatModel, SessionData

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from settings import API_Settings
from data.database import get_query_engine

import google.generativeai as genai
import google.ai.generativelanguage as glm


def get_doc_recs(doctor_type: str, location: str) -> str:
    """ get doctor recommendations ONLY when given BOTH type (speciality) of doctor and location of the user"""
    
    query_engine = get_query_engine()
    query = f'Give me all information about a doctor of {doctor_type} in {location}'
    response = query_engine.query(query)
    
    return str(response)

api_key = API_Settings.API_KEY
genai.configure(api_key=API_Settings.API_KEY)
model = genai.GenerativeModel('gemini-pro', tools=[get_doc_recs])

from uuid import uuid4
from session import backend, cookie
from fastapi import Response

@app.post("/create_chat")
async def create_chat(response: Response):
    session = uuid4()
    chat = model.start_chat(history=[])
    chat.send_message(content="You are a healthcare bot designed for recommending doctors and solving patient's queries. Your name is Max. YOU CAN ANSWER GENERAL PATIENT QUERIES. \
        You must converse with the me and gather the following fields (YOU MUST NOT MAKE ASSUMPTIONS) from our conversation: 'the speciality of doctor they should be recommended based on their symptoms (must be a normal speciality)' and 'city in which the doctor should be'. When you have ALL REQUIRED DETAILS, THEN YOU CAN RECOMMEND DOCTORS.")
    data = SessionData(chat_history=chat.history)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)
    return { "session_id": session }, 200


@app.post("/chat")
async def handle_chat(chat_model: ChatModel):
    message = chat_model.message
    session = chat_model.session_id

    session_data = await backend.read(session)
    history = session_data.chat_history

    chat = model.start_chat(history=history)  
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
    return { response.text } , 200


@app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)




