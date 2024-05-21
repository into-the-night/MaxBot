from pydantic import BaseModel, ConfigDict
from uuid import UUID
import google.generativeai as genai
from google.ai.generativelanguage import Content

class ChatModel(BaseModel):
    message: str
    session_id: UUID
    
class SessionData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    chat_history: list[Content]
