from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import router as matches_router

app = FastAPI()

# # Serve static files (e.g., profile images) from the 'static' directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(matches_router)


@app.get('/participants')
def participants():
    return [
    {
        "name": "Aarav Sharma",
        "phone": "9800001001",
        "image": "profile.webp"
    },
    {
        "name": "Sofia Rai",
        "phone": "9800001002",
        "image": "profile.webp"
    },
    {
        "name": "Rohan Thapa",
        "phone": "9800001003",
        "image": "profile.webp"
    },
    {
        "name": "Maya Gurung",
        "phone": "9800001004",
        "image": "profile.webp"
    },
    {
        "name": "Niraj Karki",
        "phone": "9800001005",
        "image": "profile.webp"
    },
    {
        "name": "Anika Shrestha",
        "phone": "9800001006",
        "image": "profile.webp"
    },
    {
        "name": "Kabir Adhikari",
        "phone": "9800001007",
        "image": "profile.webp"
    },
    {
        "name": "Priya Bhandari",
        "phone": "9800001008",
        "image": "profile.webp"
    },
    {
        "name": "Sanjay Basnet",
        "phone": "9800001009",
        "image": "profile.webp"
    },
    {
        "name": "Elina Poudel",
        "phone": "9800001010",
        "image": "profile.webp"
    }
]