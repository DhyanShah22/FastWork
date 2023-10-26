from fastapi import FastAPI, Depends, status, HTTPException
from typing import Annotated
import models
from database import engine, Sessionlocal
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

class ContentBase(BaseModel):
    name: str
    content_id: int
    content: str

class ContentPatch(ContentBase):
    content: str

def get_db():
    db = Sessionlocal()
    
    try:
        yield db

    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/content/{content_id}", status_code= status.HTTP_200_OK)
async def get_content(content_id: int, db: db_dependency):
    content = db.query(models.Content).filter(models.Content.content_id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail='Nai milrha bc')
    return content

@app.post("/content/", status_code= status.HTTP_201_CREATED)
async def add_content(db: db_dependency, content: ContentBase):
    db_content = models.Content(**content.dict())
    db.add(db_content)
    db.commit()

@app.patch("/content/{content_id}", status_code= status.HTTP_202_ACCEPTED)
async def partial_update(content_id: int, db: db_dependency, content: ContentPatch):
    if content is None:
        raise HTTPException(status_code=401, detail='Cannot update')
    
    db_pupd = db.query(models.Content).filter(models.Content.content_id == content_id).first()
    db_pupd.content = content.content

    db.add(db_pupd)
    db.commit()

@app.put("/content/{content_id}", status_code= status.HTTP_202_ACCEPTED)
async def partial_update(content_id: int, db: db_dependency, content: ContentBase):
    if content is None:
        raise HTTPException(status_code=401, detail='Cannot update')
    
    db_upd = db.query(models.Content).filter(models.Content.content_id == content_id).first()

    db_upd.content = content.content
    db_upd.content_id = content.content_id
    db_upd.name = content.name

    db.add(db_upd)
    db.commit()

@app.delete("/content/{content_id}", status_code= status.HTTP_202_ACCEPTED)
async def delete_content(content_id: int, db: db_dependency, content: ContentBase):
    db_del = db.query(models.Content).filter(models.Content.content_id == content_id).first()
    if db_del is None:
        raise HTTPException(status_code=400, detail='Cannot Delete')
    db.delete(db_del)
    db.commit()