from pydantic import BaseModel, ConfigDict
from uuid import UUID
import google.generativeai as genai


class ChatModel(BaseModel):
    message: str
    session_id: UUID
    
class SessionData(BaseModel):
    chat_history: list
