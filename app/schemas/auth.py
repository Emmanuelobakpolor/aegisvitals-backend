from pydantic import BaseModel, EmailStr
from datetime import date

class FullSignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str | None
    password: str

    date_of_birth: date | None
    sex: str | None

    emergency_name: str | None
    emergency_phone: str | None
    emergency_relationship: str | None

    conditions: str | None
    medications: str | None
    allergies: str | None

    blood_pressure: bool = False
    heart_rate: bool = False
    weight: bool = False
    blood_glucose: bool = False
    sleep: bool = False
    spo2: bool = False
