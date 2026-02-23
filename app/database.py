from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
import time 
from . config import settings

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal= sessionmaker(autocommit=False , autoflush=False, bind=engine)


Base = declarative_base()
 
def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        

 
# Database connection without using sqlalchemy 

# while True:  
          
#     try:
#         conn= psycopg.connect("user=postgres password = gauravroot host= localhost dbname= fastapi" )
#         cursor = conn.cursor()
#         print("Database connected successfully")
#         break
        
#     except Exception as error:
#         print(f"Db is not connected due to ")
#         print(f"Error is {error}")
#         time.sleep(2)
       