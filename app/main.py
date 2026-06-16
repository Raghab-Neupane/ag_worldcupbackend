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


from pydantic import BaseModel
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

class LoginPayload(BaseModel):
    usergmail: str
    password: str

from app.security import verify_password
from app.schemas import UserCreate
from app.security import hash_password

@app.post("/login")
def login(payload: LoginPayload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.usergmail == payload.usergmail).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Gmail or Password")
    return {"success": True, "message": "Login successful"}

@app.post("/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    email_normalized = payload.usergmail.strip().lower()
    existing_user = db.query(User).filter(User.usergmail == email_normalized).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Gmail is already registered")
        
    new_user = User(
        usergmail=email_normalized,
        password=hash_password(payload.password)
    )
    db.add(new_user)
    db.commit()
    return {"success": True, "message": "User registered successfully"}



