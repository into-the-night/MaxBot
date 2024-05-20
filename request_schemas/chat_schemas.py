from pydantic import BaseModel, ConfigDict
from uuid import UUID
import google.generativeai as genai



class ChatModel(BaseModel):
    message: str
    session_id: UUID
    
class SessionData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    chat_session : genai.ChatSession