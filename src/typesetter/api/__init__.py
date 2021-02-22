from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .typesetter_router import router as typesetter

app = FastAPI(
    version="0.1.0",
    title="Typesetter",
    description="Microservice that uses typesetter to produce an image from text",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"],
)

responses = {
    200: {"description": "Request was successful"},
    400: {"description": "Request was unsuccessful. Client error"},
    500: {"description": "Request was unsuccessful. Server error"},
}

app.include_router(typesetter, prefix="/typesetter", tags=["typesetter"], responses=responses)  # type: ignore
