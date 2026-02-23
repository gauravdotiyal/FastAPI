from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
import time
 


app = FastAPI()


#show the schema using pydant basemodel 
class Post(BaseModel):
    title:str
    content:str   
    published:bool


# Db connection 
while True: 
          
    try:
        conn= psycopg.connect("user=postgres password = gauravroot host= localhost dbname= fastapi" )
        cursor = conn.cursor()
        print("Database connected successfully")
        break
        
    except Exception as error:
        print(f"Db is not connected due to ")
        print(f"Error is {error}")
        time.sleep(2)
        

    
myposts= [{"title":"This is first post", "content":"This is first post content", "id":1},
        {"title":"This is second post", "content":"This is second post content", "id":2}, ]

# this is the decorator for fastapi == path, operation, function to make api request 
@app.get("/")
async def root():
    return {"message":"How are the people of the for new changes World"}


#Get all the posts 
@app.get("/posts")
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts =  cursor.fetchall()
    print(posts)
    return {"data": posts}


def find_post(id):
    for p in myposts:
        if p['id']==id:
            return p


def findIndex(id):
    for i, p in enumerate(myposts):
        if p['id']==id:
            return i


#status code for creating post is 201
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def createPost(post:Post):
    cursor.execute("""INSERT INTO posts (title, content , published) VALUES(%s , %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    new_post= cursor.fetchone()
    
    conn.commit()
    return {"data":new_post}



@app.get("/posts/{id}")
async def get_posts(id : int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, ( id, ) )
    post = cursor.fetchone() 
    if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail=f"The post with id : {id} is not found ") 
     
    return {"post_detail":post}



#Now delete post code 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int): 
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (id, ))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} does not exist" )
    
    return  Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
## Update post 
@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
async def update_post(id:int, post : Post): 
    cursor.execute(""" UPDATE posts SET title = %s, content= %s, published= %s WHERE id=%s RETURNING * """ , 
                   (post.title, post.content, post.published, id ) )
    updated_post= cursor.fetchone() 
    conn.commit()
    
    
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} does not exist" )
    
     
    return {"data":updated_post}


