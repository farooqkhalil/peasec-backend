import datetime
from sqlalchemy import Column, TEXT, Integer, BINARY, VARCHAR, Float, DateTime
from app.database import Base


class UserCreds(Base):
    __tablename__ = "user_creds"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(VARCHAR(30), unique=True)
    password = Column(BINARY(60))
    fullname = Column(VARCHAR(30))


class Report(Base):
    __tablename__ = "report"

    report_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    type = Column(VARCHAR(255))
    title = Column(VARCHAR(30))
    content = Column(VARCHAR(255))
    lng = Column(Float)
    lat = Column(Float)
    country = Column(VARCHAR(30))
    image1 = Column(TEXT)
    image2 = Column(TEXT)
    image3 = Column(TEXT)
    time_created = Column(DateTime, default=datetime.datetime.utcnow)


class Blog(Base):
    __tablename__ = "blog"

    blog_id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(30))
    content = Column(VARCHAR(255))










