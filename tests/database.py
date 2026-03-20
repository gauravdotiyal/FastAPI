## DATABASE CODE FOR TESTING ONLY 

from fastapi.testclient import TestClient
import pytest 
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker 
from app.config import settings
from app.database import get_db
from app.database import Base

#Database for testing only 

DATABASE_URL = settings.database_url+"_test"

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal= sessionmaker(autocommit=False , autoflush=False, bind=engine)


# Database testing work ends here

client= TestClient(app)

@pytest.fixture()
def session():
    # run our code after the test to drop tables 
    Base.metadata.drop_all(bind=engine)
    #run our code before the test to create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        

@pytest.fixture()
def client(session):
    def override_get_db():
         
        try:
            yield session
            
        finally:
            session.close()
        
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)