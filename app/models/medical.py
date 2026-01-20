from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class MedicalInfo(Base):
    __tablename__ = "medical_info"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    conditions = Column(String, nullable=True)
    medications = Column(String, nullable=True)
    allergies = Column(String, nullable=True)
