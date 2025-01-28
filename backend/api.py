from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import Chatbot
from knowledge_base import KnowledgeBase


app = FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




kb = KnowledgeBase()
chatbot = Chatbot(kb)


class ChatMessage(BaseModel):
    message: str


@app.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    response = chatbot.process_query(chat_message.message)
    return {"reply": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
