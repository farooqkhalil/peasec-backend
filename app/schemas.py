from pydantic import BaseModel


class UserInfoBase(BaseModel):
    username: str


class UserCreate(UserInfoBase):
    fullname: str
    password: str


class UserAuthenticate(UserInfoBase):
    password: str


class UserInfo(UserInfoBase):
    user_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class ReportBase(BaseModel):
    type: str
    content: str
    lng: float
    lat: float
    country: str
    image1: str
    image2: str
    image3: str


class ReportLoc(BaseModel):
    report_id: int
    lng: float
    lat: float

    class Config:
        orm_mode = True


class Report(ReportBase):
    report_id: int

    class Config:
        orm_mode = True






