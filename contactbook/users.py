from fastapi import APIRouter ,UploadFile, File, Depends, HTTPException, status, Query, BackgroundTasks
from cloudinary.uploader import upload
from . import schemas, crud, models, auth, email_verification
from .database import get_db
from sqlalchemy.orm import Session
import cloudinary
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

router = APIRouter()

@router.post("/upload-avatar", response_model=schemas.User)
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """
    Uploads users avatar to Cloudinary and saves URL in db.

    Args:
        file (UploadFile): Avatars file for downloading.
        db (Session): Session of data base.
        current_user (schemas.User): Authoraized user.

    Raises:
        HTTPException:
            - 500 Internal Server Error, error during downloading.

    Returns:
        schemas.User: Updated user with avatar URL.
    """
    try:
        upload_result = upload(file.file, folder="avatars")
        avatar_url = upload_result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error uploading avatar")

    current_user.avatar_url = avatar_url
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registration of the hew user.

    Args:
        user (schemas.UserCreate): User data for registration.
        db (Session): Session of data base.
        background_tasks (BackgroundTasks): Background job.

    Returns:
        schemas.User: registered user.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Generates JWT tokens for access and update for authorized user.

    Args:
        form_data (schemas.UserLogin): Data for athorization(email and password).
        db (Session): Session of data base.

    Raises:
        HTTPException:
            - 401 Unauthoraized, email/password incorrect.
            - 403 Forbidden, if user didn`t authoraize the mail.

    Returns:
        schemas.Token: object, that includes "access_token", "refresh_token" and type of token.
    """
    user = crud.get_user_by_email(db, email=form_data.email)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    refresh_token = auth.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}