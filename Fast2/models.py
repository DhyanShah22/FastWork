from sqlalchemy import Integer, String, Column
from database import Base

class Content(Base):
    __tablename__ = 'content'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    content_id = Column(Integer) 
    content = Column(String(200))