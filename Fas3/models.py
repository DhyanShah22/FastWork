from sqlalchemy import Column, String, Integer, Float
from database import Base

class Result(Base):
    __tablename__ = 'resultexam'

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer)
    name = Column(String(50))
    rollno = Column(String(50))
    subject = Column(String(50))
    marks = Column(Float)