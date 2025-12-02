from fastapi import FastAPI,Depends,HTTPException,status,Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine,select,delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import time
from pydantic import BaseModel
from typing import Optional
import models
from database import get_db,Base
from schemas import UserCreate,Token,Questions,QCreate,User,UserQ
from auth import hash_password,verify_password,decode_access_token,create_access_token
import schedule
import time
from datetime import datetime
import logging
from logger import logger
import sys

engine = create_engine('postgresql://postgres:ntltcua3006@localhost/Quizz')
Base.metadata.create_all(engine)

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.add_middleware()

#get logger
# logger = logging.getLogger()
# #create formmater
# formatter = logging.Formatter(fmt ='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# #create file handler
# stream_handler = logging.StreamHandler(sys.stdout)
# file_hanler = logging.FileHandler('app.log')
# #set formmater
# stream_handler.setFormatter(formatter)
# file_hanler.setFormatter(formatter)
# #add handler
# logger.handlers = [stream_handler,file_hanler]
# logger.setLevel(logging.INFO)

# def job():
#    job_time=logger.info('Time at now: ')
#    return job_time    
# schedule.every(5).seconds.do(job)
# while True:
#    schedule.run_pending()
#    time.sleep(1)




@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": 'Something went wrong',
            "detail": exc.detail},
    )

@app.post('/create-user/',response_model=UserCreate,status_code = status.HTTP_201_CREATED)
async def create_user(user:UserCreate,db : AsyncSession = Depends(get_db)):
    query = select(models.Users).where(models.Users.username == user.username)
    result = await db.execute(query)
    check_user = result.scalar_one_or_none()
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exists')
    user.password = hash_password(user.password)
    new_user = models.Users(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post('/login/',response_model=Token,status_code = status.HTTP_200_OK)
async def login(
                user: UserCreate,
                db : AsyncSession = Depends(get_db)):
    query = select(models.Users).where(models.Users.username == user.username)
    result = await db.execute(query)
    check_user = result.scalar_one_or_none()
    if not check_user or not verify_password(user.password,check_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='username or password is incorrect')
    user_token = create_access_token(data={'sub':str(check_user.id)})
    return {'access_token':user_token,'token_type':'bearer','status':'login successfully'}

@app.get('/get-user/{user_id}',status_code = status.HTTP_200_OK,response_model=UserQ)
async def get_user(user_id:int,db : AsyncSession = Depends(get_db)):
    query = select(models.Users).where(models.Users.id == user_id)
    result = await db.execute(query)
    check_user = result.scalar_one_or_none()
    if not check_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    query_q = select(models.Questions).where(models.Questions.user_id == user_id)
    result_q = await db.execute(query_q)
    check_question = result_q.scalars().all()
    results = UserQ(id=check_user.id,username=check_user.username,questions=check_question)
    return results
    return 

@app.get('/get-all-user/',status_code = status.HTTP_200_OK,response_model=list[User])
async def get_user(db : AsyncSession = Depends(get_db)):
    try:    
        query = select(models.Users)
        result = await db.execute(query)
        check_user = result.scalars().all()
        return check_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Somthing went wrong: {e}'
        )
    
@app.post('/create-question/',
          response_model=Questions,
          status_code = status.HTTP_201_CREATED
        )
async def create_question(question:QCreate,db : AsyncSession = Depends(get_db),current_user: int = Depends(decode_access_token)):
    new_question = models.Questions(**question.dict(),user_id=int(current_user))
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return new_question

@app.get('/get-question/{question_id}',status_code = status.HTTP_200_OK,response_model=Questions)
async def get_question(question_id:int,db : AsyncSession = Depends(get_db),current_user: int = Depends(decode_access_token)):
    query = select(models.Questions).where(models.Questions.user_id == int(current_user),models.Questions.id == question_id)
    result = await db.execute(query)
    check_question = result.scalar_one_or_none()
    if not check_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Question not found')
    return check_question

@app.get('/get-all-question/',status_code = status.HTTP_200_OK,response_model=list[Questions])
async def get_all_question(db : AsyncSession = Depends(get_db),current_user: int = Depends(decode_access_token)):
    try:
        query = select(models.Questions).where(models.Questions.user_id == int(current_user))
        result = await db.execute(query)
        check_question = result.scalars().all()
        return check_question
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Somthing went wrong: {e}'
        )
    

class questionUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None

@app.patch('/update-question/{question_id}',status_code = status.HTTP_200_OK,response_model=Questions)
async def update_question(question_id:int,question:questionUpdate,current_user: int = Depends(decode_access_token),db : AsyncSession = Depends(get_db)):
    query = select(models.Questions).where(models.Questions.id == question_id,models.Questions.user_id == int(current_user))
    result = await db.execute(query)
    check_question = result.scalar_one_or_none()
    if not check_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Question not found'
        )
    update_question = question.model_dump(exclude_unset=True)
    for key,value in update_question.items():
        setattr(check_question,key,value)
    await db.commit()
    await db.refresh(check_question)
    return check_question

@app.delete('/delete-question/{question_id}',status_code = status.HTTP_200_OK)
async def delete_question(question_id:int,db : AsyncSession = Depends(get_db),current_user: int = Depends(decode_access_token)):
    query = select(models.Questions).where(models.Questions.id == question_id,models.Questions.user_id == int(current_user))
    result = await db.execute(query)
    check_question = result.scalar_one_or_none()
    if not check_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Question not found'
        )
    await db.delete(check_question)
    await db.commit()
    return {'message':'Question deleted successfully'}

# --- 1. THÊM IMPORT MỚI ---
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel
import secrets # Để tạo mật khẩu ngẫu nhiên cho user Google

# --- 2. CẤU HÌNH ---
# Thay dòng này bằng CLIENT ID bạn vừa lấy ở Bước 1
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com"

# Schema cho body gửi lên
class GoogleLoginRequest(BaseModel):
    token: str

# --- 3. ENDPOINT XỬ LÝ ĐĂNG NHẬP GOOGLE ---
@app.post("/google-login", status_code=status.HTTP_200_OK)
async def google_login(request: GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Xác thực token với Google
        id_info = id_token.verify_oauth2_token(
            request.token, 
            google_requests.Request(), 
            GOOGLE_CLIENT_ID
        )

        email = id_info['email']
        
        # Kiểm tra xem user này đã có trong DB chưa (Dùng email làm username)
        query=select(models.User).filter(models.User.username == email)
        db_user = await db.execute(query)
        db_user = db_user.scalar_one_or_none()
        if not db_user:
            # Nếu chưa có -> Tự động Đăng ký
            # Tạo mật khẩu ngẫu nhiên vì họ dùng Google login, không cần pass
            random_password = secrets.token_urlsafe(16)
            hashed_password = hash_password(random_password)
            
            new_user = models.User(
                username=email,
                password=hashed_password
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_id = new_user.id
        else:
            user_id = db_user.id
        # Tạo Token của app mình (JWT)
        access_token = create_access_token(data={"sub": str(user_id)})
        return {"status": "login successfully", "access_token": access_token, "token_type": "bearer"}

    except ValueError:
        raise HTTPException(status_code=400, detail="Token Google không hợp lệ")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))