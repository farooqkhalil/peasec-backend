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
    type: int
    title: str
    content: str
    lng: float
    lat: float


class Report(ReportBase):
    report_id: int

    class Config:
        orm_mode = True


class BlogBase(BaseModel):
    title: str
    content: str


class Blog(BlogBase):
    blog_id: int

    class Config:
        orm_mode = True







