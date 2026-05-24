from pydantic import BaseModel, EmailStr

class RegistrationCreate(BaseModel):
    first_name: str
    last_name: str
    document_id: str
    email: EmailStr

class RegistrationRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    document_id: str
    email: EmailStr
    event_id: int

    class Config:
        orm_mode = True