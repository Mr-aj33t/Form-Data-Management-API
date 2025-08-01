# app/models.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base

class WheelSpecification(Base):
    __tablename__ = "wheel_specifications"

    id = Column(Integer, primary_key=True, index=True)
    formNumber = Column(String, unique=True, index=True)
    submittedBy = Column(String)
    submittedDate = Column(Date)
    fields = Column(JSONB)
    status = Column(String, default="Saved")

    def __repr__(self):
        return f"<WheelSpecification(id={self.id}, formNumber='{self.formNumber}')>"

class BogieChecksheet(Base):
    __tablename__ = "bogie_checksheets"

    id = Column(Integer, primary_key=True, index=True)
    formNumber = Column(String, unique=True, index=True)
    submittedBy = Column(String)
    submittedDate = Column(Date)
    fields = Column(JSONB)
    status = Column(String, default="Saved")

    def __repr__(self):
        return f"<BogieChecksheet(id={self.id}, formNumber='{self.formNumber}')>"