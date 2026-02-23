
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from .. import schemas, utils, models
from ..database import get_db
from sqlalchemy.orm import Session

router= APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Working with users 
@router.post("/", status_code=status.HTTP_201_CREATED ,response_model=schemas.UserOut)
async def createUser(user:schemas.UserCreate, db: Session= Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    user= models.User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
      
    return  user


@router.get("/{id}", response_model=schemas.UserOut)
async def getUserById(id:int, db:Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Use with id : {id} does not exist" )
        
    return user 
