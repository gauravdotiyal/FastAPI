from pydantic import BaseModel, EmailStr
from datetime import datetime 
from typing import Optional 
from pydantic import conint
from typing import Literal

# We use pydantic models for request and response data handling 
#show the schema using pydant basemodel 
class PostBase(BaseModel):
    title:str
    content:str   
    published:bool = True
    
    
class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    email:str
    id:int 
    created_at:datetime
    class Config:
        orm_model=True
        
class Post(PostBase):
    id:int
    created_at:datetime    
    owner_id:int
    owner:UserOut
    class Config:
        orm_mode=True
        

class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:EmailStr
    password:str
    

class Token(BaseModel):
    access_token:str 
    token_type:str 
    
class TokenData(BaseModel):
    id : Optional[int]=None
    

class Vote(BaseModel):
    post_id:int
    dir: Literal[0,1]
    

class PostOut(BaseModel):
    Post:Post
    votes:int
    
    class Config:
        orm_mode=True