
from pydantic import BaseModel, EmailStr
from typing import Optional

class WorkerModel(BaseModel):
    id: Optional[int] = None 
    name: str
    description: str
    category: str
    rating: float
    reviews: int
    available: bool
    image: str
    provider_name: str
    provider_village: str
    provider_contact: str
    gender: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "customer"
    image: str = ""
    contact: str = None
    location: str = None
    gender: str = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BookingCreate(BaseModel):
    customer_id: int
    worker_id: int
    customer_name: str = None
    worker_name: str = None
    location: str = None
    price: float = None
    date: str
    status: str = "Pending"
    contact: str = None
    description_work: str = None
    service: str = None

class TranslationRequest(BaseModel):
    text: str
    target_lang: str