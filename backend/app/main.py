from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.db.mongodb import close_mongo_connection, connect_to_mongo
from .core.config import settings
from .api.v1.api import api_router
from .core.logger import log_info

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await connect_to_mongo() 

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "healthy"}