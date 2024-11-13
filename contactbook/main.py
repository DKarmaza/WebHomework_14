from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud, auth
from .database import engine, get_db
from .users import router as user_router
from ratelimit import init_rate_limiter
from fastapi_limiter.depends import RateLimiter

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    await init_rate_limiter(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/users", tags=["users"])

@app.get("/contacts/", response_model=List[schemas.ContactInDB])
def read_contacts(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    return crud.get_contacts_by_user(db, user_id=current_user.id)

@app.post("/contacts/", response_model=schemas.ContactInDB, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    return crud.create_contact(db, contact=contact, user_id=current_user.id)

@app.put("/contacts/{contact_id}", response_model=schemas.ContactInDB)
def update_contact(
    contact_id: int,
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):

    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None or db_contact.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found or not owned by user")
    
    return crud.update_contact(db, db_contact, contact)

@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):

    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None or db_contact.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found or not owned by user")
    
    crud.delete_contact(db, db_contact)
    return {"detail": "Contact deleted"}
