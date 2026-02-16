from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "YourUserName://postgres:YourPassword@localhost:5432/karyanet"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
