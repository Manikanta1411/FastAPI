from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.middleware.cors import CORSMiddleware

# ------------------- DATABASE SETUP -------------------

engine = create_engine("mysql+pymysql://root:Manikanta2001@localhost/customerdetails")
Session = sessionmaker(bind=engine)
Base = declarative_base()

# ------------------- MODEL -------------------
class Detail(Base):
    __tablename__ = "details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    mobile = Column(String(15), nullable=False)

Base.metadata.create_all(engine)

# ------------------- APP -------------------
app = FastAPI(title="Customer Details API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ------------------- ROUTES -------------------

# ===== ADD DETAIL =====
@app.post("/add_detail")
async def add_detail(request: Request):
    data = await request.json()
    name = data.get("name")
    email = data.get("email")
    mobile = data.get("mobile")

    if not all([name, email, mobile]):
        return JSONResponse({"error": "All fields (name, email, mobile) are required"}, status_code=400)

    session = Session()
    new_detail = Detail(name=name, email=email, mobile=mobile)
    session.add(new_detail)
    session.commit()
    session.refresh(new_detail)
    session.close()

    return JSONResponse({"message": "Detail added successfully", "id": new_detail.id}, status_code=201)

# ===== GET ALL DETAILS =====
@app.get("/get_details")
def get_details():
    session = Session()
    details = session.query(Detail).all()
    result = [{"id": d.id, "name": d.name, "email": d.email, "mobile": d.mobile} for d in details]
    session.close()
    return JSONResponse(result, status_code=200)

# ===== GET SINGLE DETAIL =====
@app.get("/get_detail/{id}")
def get_detail(id: int):
    session = Session()
    detail = session.query(Detail).filter_by(id=id).first()
    session.close()
    if detail:
        return JSONResponse({"id": detail.id, "name": detail.name, "email": detail.email, "mobile": detail.mobile}, status_code=200)
    return JSONResponse({"error": "Detail not found"}, status_code=404)

# ===== UPDATE DETAIL =====
@app.put("/update_detail/{id}")
async def update_detail(id: int, request: Request):
    data = await request.json()
    session = Session()
    detail = session.query(Detail).filter_by(id=id).first()
    if not detail:
        session.close()
        return JSONResponse({"error": "Detail not found"}, status_code=404)

    detail.name = data.get("name", detail.name)
    detail.email = data.get("email", detail.email)
    detail.mobile = data.get("mobile", detail.mobile)

    session.commit()
    session.close()
    return JSONResponse({"message": "Detail updated successfully"}, status_code=200)

# ===== DELETE DETAIL =====
@app.delete("/delete_detail/{id}")
def delete_detail(id: int):
    session = Session()
    detail = session.query(Detail).filter_by(id=id).first()
    if not detail:
        session.close()
        return JSONResponse({"error": "Detail not found"}, status_code=404)

    session.delete(detail)
    session.commit()
    session.close()
    return JSONResponse({"message": "Detail deleted successfully"}, status_code=200)

# ===== HOME =====
@app.get("/")
def home():
    return JSONResponse({"message": "Customer Details API is running"}, status_code=200)
