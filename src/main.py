import uvicorn
from fastapi import FastAPI

import database.router as dbRouter
import admin.router as adminRouter

app = FastAPI()
app.include_router(dbRouter.router)
app.include_router(adminRouter.router)

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)