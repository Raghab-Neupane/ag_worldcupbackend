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
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)  # NOTE: Do not add /calculate or /getresult routes here; they will be handled by a separate service. Use an environment variable (e.g., CALC_SERVICE_URL) in the frontend to fetch those endpoints.


@app.on_event("startup")
def on_startup():
    init_db()


from app.calculate import router as calculate_router
app.include_router(calculate_router)
app.include_router(matches_router)


