from fastapi import FastAPI
from routers import spycats, missions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(spycats.router)
app.include_router(missions.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
