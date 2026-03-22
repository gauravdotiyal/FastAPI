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
from app.oauth2 import create_access_token
from app import models

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

# Need a fixture for returning the user 
@pytest.fixture()
def test_user2(client):
    user_data={"email":"gaurav123@gmail.com", "password":"1234"}
    res= client.post("/users/", json=user_data)
    
    assert res.status_code==201
    print(res.json())
    new_user=res.json()
    new_user["password"]=user_data["password"]
    return new_user   

# Need a fixture for returning the user 
@pytest.fixture()
def test_user(client):
    user_data={"email":"gaurav@gmail.com", "password":"1234"}
    res= client.post("/users/", json=user_data)
    
    assert res.status_code==201
    print(res.json())
    new_user=res.json()
    new_user["password"]=user_data["password"]
    return new_user

@pytest.fixture() 
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture() 
def authorized_client(client, token):
    client.headers= {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    
    return client


# This is fixture for creating posts for testing
@pytest.fixture
def test_posts(test_user, session,test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user['id']
    },
        {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user['id']
    },
    {
        "title": "fourth title",
        "content": "fourht content",
        "owner_id": test_user2['id']
    }
    ]
    
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts=list(post_map)
    
    session.add_all(posts)
    
    # session.add_all([models.Post(title="first_title", content="first content", owner_id=test_user["id"]), 
    #                  models.Post(title="second title", content="second content", owner_id=test_user["id"]),
    #                  models.Post(title="third_title", content="third content", owner_id=test_user["id"])])
   
    session.commit()
    
    posts= session.query(models.Post).all()
    return posts