from fastapi import FastAPI
from typing import List
from fastapi import Body 
from . import models 
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine) 
        
app = FastAPI() 

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

    
# this is the decorator for fastapi == path, operation, function to make api request 
@app.get("/")
async def root():
    return {"message":"How are the people of the for new changes World"}


