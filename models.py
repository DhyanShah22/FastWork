from sqlalchemy import Integer, String, Float, Column
from database import Base

class Workshop(Base):
    __tablename__ = 'workshop'

    id = Column(Integer, primary_key=True, index=True)
    workshop_id = Column(Integer)
    name = Column(String(100))
    batch = Column(Integer)
    rollno = Column(String(50))
    