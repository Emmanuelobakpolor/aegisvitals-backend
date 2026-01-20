from sqlalchemy import Column, Integer, Date, String, ForeignKey
from app.core.database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    date_of_birth = Column(Date, nullable=True)
    sex = Column(String, nullable=True)
