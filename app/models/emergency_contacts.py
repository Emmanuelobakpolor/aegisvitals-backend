from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    relationship = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
