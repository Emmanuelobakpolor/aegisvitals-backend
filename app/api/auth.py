from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.models.profile import UserProfile
from app.models.emergency_contacts import EmergencyContact
from app.models.medical import MedicalInfo
from app.models.goals import HealthGoals
from app.schemas.auth import FullSignupRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/register-full")
async def register_full(data: FullSignupRequest, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(User).where(User.email == data.email))
        if result.scalar():
            raise HTTPException(status_code=400, detail="Email already exists")

        user = User(
            full_name=data.full_name,
            email=data.email,
            phone_number=data.phone_number,
            password_hash=hash_password(data.password),
        )
        db.add(user)
        await db.flush()

        db.add(UserProfile(
            user_id=user.id,
            date_of_birth=data.date_of_birth,
            sex=data.sex,
        ))

        if data.emergency_name:
            if not data.emergency_phone:
                raise HTTPException(status_code=400, detail="Emergency phone number is required")
            db.add(EmergencyContact(
                user_id=user.id,
                name=data.emergency_name,
                phone_number=data.emergency_phone,
                relationship=data.emergency_relationship,
            ))

        db.add(MedicalInfo(
            user_id=user.id,
            conditions=data.conditions,
            medications=data.medications,
            allergies=data.allergies,
        ))

        db.add(HealthGoals(
            user_id=user.id,
            blood_pressure=data.blood_pressure,
            heart_rate=data.heart_rate,
            weight=data.weight,
            blood_glucose=data.blood_glucose,
            sleep=data.sleep,
            spo2=data.spo2,
        ))

    return {"message": "Signup completed successfully"}

@router.post("/login")
async def login(data: dict, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data["email"]))
    user = result.scalar()

    if not user or not verify_password(data["password"], user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    profile_result = await db.execute(select(UserProfile).where(UserProfile.user_id == user.id))
    profile = profile_result.scalar()

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number,
        },
        "profile": {
            "date_of_birth": profile.date_of_birth,
            "sex": profile.sex,
        } if profile else None,
    }
