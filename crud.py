
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Message, User
from database import SessionLocal
from schemas import MessageCreate, MessageRead
import uuid
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
message_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid auth")
        user = db.query(User).filter(User.username == username).first()
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@message_router.post("/", response_model=MessageRead)
def create_message(message: MessageCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    msg_id = str(uuid.uuid4())
    db_message = Message(id=msg_id, encrypted_message=message.encrypted_message, sender_id=user.id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@message_router.get("/{id}", response_model=MessageRead)
def read_message(id: str, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()
    return message
