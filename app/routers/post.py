from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func 

router= APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


#Get all the posts 
@router.get("/",response_model=List[schemas.PostOut])
async def get_posts(db : Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit:int= 10, skip : int = 0, search :Optional[str]=""):   
    # print(limit)
      
    # posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    
    return posts


#status code for creating post is 201
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def createPost(post:schemas.PostCreate,db : Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)): 
    
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id,  **post.model_dump())  # This is the actual way to avoid to one by one update
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post



@router.get("/{id}",response_model=schemas.PostOut)
async def get_posts(id : int, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)): 
    
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    result=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail=f"The post with id : {id} is not found ") 
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    print(result)
    return result


#Now delete post code 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, db:Session= Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):  
    
    post= db.query(models.Post).filter(models.Post.id==id)
    
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} does not exist" )
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return  Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
## Update post 
@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_post(id:int, updated_post : schemas.PostCreate, db:Session= Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):  
    
    post_query=db.query(models.Post).filter(models.Post.id==id)
    
    post= post_query.first()
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} does not exist" )
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    # post_query.update({'title':'Updated post', 'content':'This is the updated content'}, synchronize_session=False)
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    
    return post_query.first()



