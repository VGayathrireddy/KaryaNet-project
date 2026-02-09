
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

Base = declarative_base()

class Worker(Base):

    __tablename__ = "Workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    rating = Column(Float, default=0.0)
    reviews = Column(Integer, default=0)  # or JSON/text if storing review texts
    available = Column(Boolean, default=True)
    image = Column(String, default="")  # profile image URL
    provider_name = Column(String)
    provider_village = Column(String)
    provider_contact = Column(String)
    gender = Column(String)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)  # ❌ remove unique=True
    password = Column(String, nullable=False)
    role = Column(String, default="customer")
    image = Column(String, default="")  # profile image
    contact = Column(String, nullable=True)
    location = Column(String, nullable=True)  # village
    gender = Column(String, nullable=True)

    # ✅ composite unique constraint
    __table_args__ = (
        UniqueConstraint("email", "role", name="uq_user_email_role"),
    )

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("Workers.id"), nullable=False)
    customer_name = Column(String)
    worker_name = Column(String)
    location = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    date = Column(String, nullable=False)
    status = Column(String, default="Pending")  # Pending, Accepted, Completed
    contact = Column(String, nullable=True)
    description_work = Column(String, nullable=True)
    service = Column(String, nullable=True)

    customer = relationship("User", backref="bookings")
    worker = relationship("Worker", backref="bookings")
