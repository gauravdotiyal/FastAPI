from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange




app = FastAPI()


#show the schema using pydant basemodel 
class Post(BaseModel):
    title:str
    content:str 
    isValid:bool = True
    rating:Optional[int] = 1

    
myposts= [{"title":"This is first post", "content":"This is first post content", "id":1},
        {"title":"This is second post", "content":"This is second post content", "id":2}, ]

# this is the decorator for fastapi == path, operation, function to make api request 
@app.get("/")
async def root():
    return {"message":"How are the people of the for new changes World"}


#Get all the posts 
@app.get("/posts")
async def get_posts():
    return {"data": myposts}


# Helper functions for finding post in array 
def find_post(id):
    for p in myposts:
        if p['id']==id:
            return p
        
def findIndex(id):
    for i, p in enumerate(myposts):
        if p['id']==id:
            return i


# It is without using pydantic 
# @app.post("/createposts") 
# async def put_posts(payload: dict = Body(...)):
#     print(f"{payload}")
#     return {f"Tile is {payload["title"]} and the righs are {payload['rights']}"}

# It is with using pydantic 
@app.post("/posts")
async def create_post(post:Post): 
    print(post.model_dump())
    return {"data": post}

#status code for creating post is 201
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def createPost(post:Post):
    post_dict= post.model_dump()
    post_dict['id']=randrange(0,100000)
    myposts.append(post_dict)
    return {"data":post_dict}


@app.get("/posts/{id}")
async def get_posts(id : int, res:Response):
    post = find_post(id)
    if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail=f"The post with id : {id} is not found ")
    #     res.status_code=status.HTTP_404_NOT_FOUND
    #     return {"message":f"The post with id : {id} is not found "}
        
    return {"data":post}



#Now delete post code 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    # first find the post with the given id
    # second find the index of that post 
    # post.pop(index) for deleting the post from the array 
    index= findIndex(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} does not exist" )
    myposts.pop(index)
    
    return  Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
## Update post 
@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
async def update_post(id:int, post : Post):
    # Find the index of that post 
    # update the id 
    index= findIndex(id)
    
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} does not exist" )
    
    postdict=post.model_dump()
    postdict['id']=id
    myposts[index]=postdict
    return {"data":f"The updated data is {postdict}"}