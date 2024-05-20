from settings import API_Settings
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import VectorStoreIndex

api_key = API_Settings.API_KEY
embed_model = GeminiEmbedding(model_name="models/embedding-001", api_key=api_key)
Settings.embed_model = embed_model
Settings.llm = Gemini(api_key=api_key, temperature=0.7, model='models/gemini-pro')

def get_query_engine():
    
    documents = SimpleDirectoryReader(input_files=["doctor.csv"])
    documents = documents.load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(similarity_top_k=3)

    return query_engine