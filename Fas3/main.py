from fastapi import FastAPI, Depends, status, HTTPException
from typing import Annotated
from database import engine, Sessionlocal
import models
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ResultBase(BaseModel):
    result_id : int
    name: str
    rollno: str
    subject: str
    marks: float

class ResultUpdate(ResultBase):
    marks: float

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/result/{result_id}", status_code= status.HTTP_200_OK)
async def get_result(result_id: int, db: db_dependency):
    result = db.query(models.Result).filter(models.Result.result_id == result_id).first()
    if result is None:
        raise HTTPException(status_code= 404, detail='No such result detail available')
    return result

@app.post("/result/", status_code= status.HTTP_201_CREATED)
async def add_result(db: db_dependency, result: ResultBase):
    db_res = models.Result(**result.dict())
    db.add(db_res)
    db.commit()

@app.patch("/result/{result_id}", status_code= status.HTTP_202_ACCEPTED)
async def partial_update(db: db_dependency, result: ResultUpdate, result_id: int):
    if result is None:
        raise HTTPException(status_code=400, detail='Cannot Patch')
    db_pupd = db.query(models.Result).filter(models.Result.result_id == result_id).first()
    db_pupd.marks = result.marks
    db.add(db_pupd)
    db.commit()

@app.put("/result/{result_id}", status_code= status.HTTP_202_ACCEPTED)
async def update_result(db: db_dependency, result: ResultBase, result_id: int):
    if result is None:
        raise HTTPException(status_code=400, detail='Cannot Update')
    db_upd = db.query(models.Result).filter(models.Result.result_id == result_id).first()
    db_upd.marks = result.marks
    db_upd.name = result.name
    db_upd.result_id = result.result_id
    db_upd.subject = result.subject
    db_upd.rollno = result.rollno
    db.add(db_upd)
    db.commit()

@app.delete("/result/{result_id}", status_code= status.HTTP_200_OK)
async def delete_result(result_id: int, db: db_dependency):
    db_del = db.query(models.Result).filter(models.Result.result_id == result_id).first()
    if db_del is None:
        raise HTTPException(status_code=400, detail='Unable to delete')
    db.delete(db_del)
    db.commit()
    



