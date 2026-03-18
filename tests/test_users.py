## TESTING FOR USERS ONLY 

from app import schemas
from .database import client, session 

def test_root(client):
    res=client.get("/")
    print(res.json().get("status")) 
    assert res.json().get("status")=="ok"
    

def test_create_user(client):
    res= client.post("/users/", json={"email": "hdddd@gmail.com" , "password":"12443" })
    new_user = schemas.UserOut(**res.json())
    assert new_user.email=="hdddd@gmail.com"
    assert res.status_code==201
   
    

def test_login(client):
    res= client.post("/login", data={"username": "hdddd@gmail.com" , "password":"12443" })
    print(res.json())
    assert res.status_code==200