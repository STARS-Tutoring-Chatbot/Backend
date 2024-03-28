import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import openAI.router as openAI
import extractor.router as extractorRouter

app = FastAPI()
app.include_router(openAI.router)
app.include_router(extractorRouter.router)
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
