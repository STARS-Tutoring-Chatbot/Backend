import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import openAI.router as openAI
import langchainAPI.router as langchain

app = FastAPI()
app.include_router(openAI.router)
app.include_router(langchain.router)
origins = [
    "http://localhost:5173",
    os.getenv("OPEN_AI_DEV_KEY"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
