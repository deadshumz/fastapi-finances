from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserOut(UserBase):

    class Config:
        from_attributes = True
