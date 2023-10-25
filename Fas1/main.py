from fastapi import FastAPI, Depends, status, HTTPException
from typing import Annotated
import models
from database import engine, Sessionlocal
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()
models.Base.metadata.create_all(bind= engine)

class WorkBase(BaseModel):
    name: str
    batch: int
    rollno: str
    workshop_id: int

class WorkUpdate(WorkBase):
    batch: int
    rollno: str

def get_db():
    db = Sessionlocal()
    try:
        yield db

    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/work/{work_id}", status_code= status.HTTP_202_ACCEPTED)
async def get_work(work_id: int, db: db_dependency):
   work = db.query(models.Workshop).filter(models.Workshop.workshop_id == work_id).first() 
   if work is None:
       raise HTTPException(status_code=404, detail='No workshop detail found')
   return work

@app.post("/work/", status_code= status.HTTP_201_CREATED)
async def add_work(work: WorkBase, db: db_dependency):
    db_work = models.Workshop(**work.dict())
    db.add(db_work)
    db.commit()

@app.patch("/work/{work_id}", status_code=status.HTTP_200_OK)
async def partial_update(work_id: int, db: db_dependency, work: WorkUpdate):
    if work is None:
        raise HTTPException(status_code=401, detail='Cannot update')
    db_pupd = db.query(models.Workshop).filter(models.Workshop.workshop_id == work_id).first()

    db_pupd.batch = work.batch
    db_pupd.rollno = work.rollno
    db.add(db_pupd)
    db.commit()

@app.put("/works/{work_id}", status_code= status.HTTP_202_ACCEPTED)
async def update_work(work_id: int, work: WorkBase, db: db_dependency):
    if work is None:
        raise HTTPException(status_code=401, detail='Cannot find the workshop detail')
    db_upd = db.query(models.Workshop).filter(models.Workshop.workshop_id == work_id).first()

    db_upd.name = work.name
    db_upd.batch = work.batch
    db_upd.rollno = work.rollno
    db_upd.workshop_id = work.workshop_id

    db.add(db_upd)
    db.commit()

@app.delete("/workshop/{work_id}", status_code= status.HTTP_200_OK)
async def delete_work(work_id: int, db: db_dependency):
    db_del = db.query(models.Workshop).filter(models.Workshop.workshop_id == work_id).first()
    if db_del is None:
        raise HTTPException(status_code=404, detail='No workshop detail found')
    db.delete(db_del)
    db.commit()
