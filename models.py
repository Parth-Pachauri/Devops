from sqlalchemy import Column, Integer, String
from database import Base

class Calculation(Base):
    __tablename__ = "calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    num1 = Column(Integer)
    num2 = Column(Integer)
    result = Column(Integer)
