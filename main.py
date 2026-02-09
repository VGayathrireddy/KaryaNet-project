
from fastapi import Depends, FastAPI, HTTPException
from models import WorkerModel, UserCreate, UserLogin, BookingCreate, TranslationRequest
from database import session, engine
from database_models import Worker, User, Booking
import database_models
from sqlalchemy.orm import Session 
from passlib.context import CryptContext
from typing import List
from googletrans import Translator

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BCRYPT_MAX_LENGTH = 72  # bcrypt max password length

translator = Translator()

@app.get("/")

def greet():
    return "Welcome to KaryaNet"

workers = [
    WorkerModel(id=1, name="Tractor Rental", description="Rent a tractor for your farming needs with flexible pricing and reliable operators.", category="Farming", rating=4.8, available=True, reviews=0, image="", provider_name="Ram Kumar", provider_village="Village A", provider_contact="9876543210", gender="Male"),
    WorkerModel(id=2, name="Plumbing", description="Local plumbers available for all kinds of repair and maintenance work.", category="Household", rating=4.6, available=True, reviews=0, image="", provider_name="Sita Reddy", provider_village="Village B", provider_contact="9876543211", gender="Female"),
    WorkerModel(id=3, name="Mechanic", description="A rural Mechanic who fixes vehicles, etc.", category="Household", rating=4.2, available=True, reviews=0, image="", provider_name="Vikram", provider_village="Village C", provider_contact="9876543212", gender="Male"),
    WorkerModel(id=4, name="Construction Work", description="Construction work helper.", category="Construction", rating=4.1, available=True, reviews=0, image="", provider_name="Ravi", provider_village="Village D", provider_contact="9876543213", gender="Male")
]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(Worker).count()
    
    if count == 0:
        for worker in workers:
            db.add(database_models.Worker(**worker.model_dump()))
        db.commit()
    db.close()

init_db()

# Get all workers
@app.get("/workers", response_model=List[WorkerModel])
def get_all_workers(db: Session = Depends(get_db)):
    db_workers = db.query(Worker).all()
    #query
    # db.query()
    return db_workers

# Get worker by ID
@app.get("/worker/{id}", response_model=WorkerModel)
def get_worker_by_id(id: int, db: Session = Depends(get_db)):
    db_worker = db.query(Worker).filter(Worker.id == id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker Not Found")
    return db_worker

# Add new worker
@app.post("/worker", response_model=WorkerModel)
def add_worker(worker: WorkerModel, db: Session = Depends(get_db)):
    # exclude_unset=True → ignore fields not sent by frontend (like id)
    db_worker = Worker(**worker.model_dump(exclude_unset=True))
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)  # ✅ gets auto-generated ID from DB
    return db_worker       # ✅ return the saved worker (with ID)

# Update worker
@app.put("/worker/{id}")
def update_worker(id: int, worker: WorkerModel, db: Session = Depends(get_db)):
    db_worker = db.query(Worker).filter(Worker.id == id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    for field, value in worker.model_dump().items():
        setattr(db_worker, field, value)
    
    db.commit()
    return {"message": "Worker updated", "worker_id": id}


#DElete Worker
@app.delete("/worker/{id}")
def delete_worker(id: int, db: Session = Depends(get_db)):
    db_worker = db.query(Worker).filter(Worker.id == id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    db.delete(db_worker)
    db.commit()
    return {"message": "Worker deleted"}
    
# Helper function to safely hash passwords
def hash_password(password: str) -> str:
    # This is correct: Truncate the string *before* hashing.
    # passlib handles the encoding.
    safe_password = password[:BCRYPT_MAX_LENGTH] 
    return pwd_context.hash(safe_password)


# Register
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw,
        role=user.role,
        image=user.image,
        contact=user.contact,
        location=user.location,
        gender=user.gender
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully", "user_id": db_user.id}


# Login
@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    safe_password = user.password[:BCRYPT_MAX_LENGTH]
    if not pwd_context.verify(safe_password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "name": db_user.name,
        "role": db_user.role   # NEW
    }


#For create bookings
@app.post("/book-service")
def book_service(booking: BookingCreate, db: Session = Depends(get_db)):
    # Optionally fetch worker and customer names if not provided
    if not booking.customer_name:
        customer = db.query(User).filter(User.id == booking.customer_id).first()
        booking.customer_name = customer.name if customer else "Unknown"

    if not booking.worker_name:
        worker = db.query(Worker).filter(Worker.id == booking.worker_id).first()
        booking.worker_name = worker.name if worker else "Unknown"
    
    db_booking = Booking(**booking.model_dump()) # Use .model_dump()
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return {"message": "Booking created", "booking_id": db_booking.id}

#get bookings
# Get bookings
@app.get("/bookings")
def get_bookings(customer_id: int = None, worker_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Booking)
    if customer_id:
        query = query.filter(Booking.customer_id == customer_id)
    if worker_id:
        query = query.filter(Booking.worker_id == worker_id)
    
    bookings = query.all()
    
    # Return all important details
    result = []
    for b in bookings:
        result.append({
            "booking_id": b.id,
            "customer_id": b.customer_id,
            "customer_name": b.customer_name,
            "worker_id": b.worker_id,
            "worker_name": b.worker_name,
            "description": b.description_work,
            "location": b.location,
            "price": b.price,
            "status": b.status,
            "contact": b.contact,
            "date": b.date,
            "service": b.service
        })
    return result



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate")
def translate_text(request: TranslationRequest):
    result = translator.translate(request.text, dest=request.target_lang)  # <-- and here
    return {"translated_text": result.text}