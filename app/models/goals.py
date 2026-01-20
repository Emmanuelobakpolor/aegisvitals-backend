from sqlalchemy import Column, Integer, Boolean, ForeignKey
from app.core.database import Base

class HealthGoals(Base):
    __tablename__ = "health_goals"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    blood_pressure = Column(Boolean, default=False)
    heart_rate = Column(Boolean, default=False)
    weight = Column(Boolean, default=False)
    blood_glucose = Column(Boolean, default=False)
    sleep = Column(Boolean, default=False)
    spo2 = Column(Boolean, default=False)
