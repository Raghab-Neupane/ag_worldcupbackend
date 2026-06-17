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


@app.get('/result')
def result_list():
    return {
    "participants": [
        {
            "customer_id": "894314",
            "name": "Shahadev",
            "mobile_number": "9768447169"
        },
        {
            "customer_id": "594813",
            "name": "Anuj Bhatt",
            "mobile_number": "9767440260"
        },
        {
            "customer_id": "403182",
            "name": "Sabina Adhikari",
            "mobile_number": "9847040732"
        },
        {
            "customer_id": "938923",
            "name": "BASHANT GHIMIRE",
            "mobile_number": "9765955342"
        },
        {
            "customer_id": "938923",
            "name": "BASHANT GHIMIRE",
            "mobile_number": "9765955342"
        },
        {
            "customer_id": "938923",
            "name": "BASHANT GHIMIRE",
            "mobile_number": "9765955342"
        },
        {
            "customer_id": "938923",
            "name": "BASHANT GHIMIRE",
            "mobile_number": "9765955342"
        },
        {
            "customer_id": "938923",
            "name": "BASHANT GHIMIRE",
            "mobile_number": "9765955342"
        },
        {
            "customer_id": "938923",
            "name": "BASHANT GHIMIRE",
            "mobile_number": "9765955342"
        },
        {
            "customer_id": "938923",
            "name": "BASHANT GHIMIRE",
            "mobile_number": "9765955342"
        },
        {
            "customer_id": "944248",
            "name": "Alina Lammiichhane Thapa magar",
            "mobile_number": "9704204132"
        },
        {
            "customer_id": "900273",
            "name": "Rohit",
            "mobile_number": "9749401768"
        },
        {
            "customer_id": "899771",
            "name": "Aditya Mehata",
            "mobile_number": "9713104740"
        },
        {
            "customer_id": "899771",
            "name": "Aditya Mehata",
            "mobile_number": "9713104740"
        },
        {
            "customer_id": "457430",
            "name": "Karina Moktan",
            "mobile_number": "9860052355"
        },
        {
            "customer_id": "941250",
            "name": "Prince Tiwari",
            "mobile_number": "9701373816"
        },
        {
            "customer_id": "594813",
            "name": "Anuj Bhatt",
            "mobile_number": "9767440260"
        },
        {
            "customer_id": "950426",
            "name": "shubham",
            "mobile_number": "9768990522"
        },
        {
            "customer_id": "755101",
            "name": "Jasmine Sunam",
            "mobile_number": "9707932938"
        },
        {
            "customer_id": "505183",
            "name": "Chiranjibi Chaudhary",
            "mobile_number": "9848657493"
        },
        {
            "customer_id": "592289",
            "name": "Aayushree Joshi",
            "mobile_number": "9841530440"
        },
        {
            "customer_id": "782980",
            "name": "Sujan Chhetrii",
            "mobile_number": "9702303110"
        },
        {
            "customer_id": "287213",
            "name": "Bibhus Shrestha",
            "mobile_number": "9847972401"
        },
        {
            "customer_id": "950615",
            "name": "9844145523",
            "mobile_number": "9844145523"
        },
        {
            "customer_id": "740622",
            "name": "Prekshya Thapa",
            "mobile_number": "9847757227"
        },
        {
            "customer_id": "581767",
            "name": "Sarthak Niraula",
            "mobile_number": "9862021855"
        },
        {
            "customer_id": "894314",
            "name": "Shahadev",
            "mobile_number": "9768447169"
        },
        {
            "customer_id": "950776",
            "name": "9761262633",
            "mobile_number": "9761262633"
        },
        {
            "customer_id": "704209",
            "name": "Kismat Subedi",
            "mobile_number": "9766618300"
        },
        {
            "customer_id": "403182",
            "name": "Sabina Adhikari",
            "mobile_number": "9847040732"
        },
        {
            "customer_id": "942804",
            "name": "Rojal poudel",
            "mobile_number": "9860770061"
        },
        {
            "customer_id": "142041",
            "name": "Nirmal Mahato",
            "mobile_number": "9827986662"
        },
        {
            "customer_id": "615114",
            "name": "Sabin Belbase",
            "mobile_number": "9807533881"
        },
        {
            "customer_id": "949473",
            "name": "Shubham Subedi",
            "mobile_number": "9845368302"
        },
        {
            "customer_id": "212353",
            "name": "Sushan Marasini",
            "mobile_number": "9846579137"
        },
        {
            "customer_id": "210023",
            "name": "Suresh Shah",
            "mobile_number": "9841461367"
        },
        {
            "customer_id": "853709",
            "name": "Pramod Neupane",
            "mobile_number": "9743439244"
        },
        {
            "customer_id": "942804",
            "name": "Rojal poudel",
            "mobile_number": "9860770061"
        },
        {
            "customer_id": "910102",
            "name": "Supriya",
            "mobile_number": "9864428569"
        },
        {
            "customer_id": "600942",
            "name": "Kaniska Bhandari",
            "mobile_number": "9701875867"
        },
        {
            "customer_id": "304225",
            "name": "Sugam Rijal",
            "mobile_number": "9867505392"
        },
        {
            "customer_id": "578996",
            "name": "Sudip Chaudhary",
            "mobile_number": "9704014811"
        },
        {
            "customer_id": "133223",
            "name": "zzz",
            "mobile_number": "9805847786"
        },
        {
            "customer_id": "133223",
            "name": "zzz",
            "mobile_number": "9805847786"
        },
        {
            "customer_id": "878966",
            "name": "Subodh Subedi",
            "mobile_number": "9847263615"
        },
        {
            "customer_id": "766779",
            "name": "Chiranjibi Shahi",
            "mobile_number": "9868910249"
        },
        {
            "customer_id": "943037",
            "name": "Ganesh",
            "mobile_number": "9867601097"
        },
        {
            "customer_id": "403182",
            "name": "Sabina Adhikari",
            "mobile_number": "9847040732"
        },
        {
            "customer_id": "384480",
            "name": "Arix",
            "mobile_number": "9814630631"
        },
        {
            "customer_id": "952280",
            "name": "Prakash Kunwar",
            "mobile_number": "9743239249"
        },
        {
            "customer_id": "68012",
            "name": "Gorkha King",
            "mobile_number": "9806644935"
        }
    ],
    "winner": {
        "customer_id": "136",
        "name": "Kishan Shrestha",
        "photo": "",
        "points": 100,
        "mobile_number": "9841924024",
        "comment": "mexico 2-0 south africa",
        "created_at": "2026-06-11T15:59:08",
        "updated_at": "2026-06-11T15:59:08"
    }
}
