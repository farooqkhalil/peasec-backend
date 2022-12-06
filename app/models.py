import sqlalchemy.dialects.mysql
from sqlalchemy import Column, Integer, String, BINARY, Text, VARCHAR, VARBINARY, CHAR, LargeBinary
from app.database import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(VARCHAR(30), unique=True)
    password = Column(BINARY(60))
    fullname = Column(VARCHAR(30), unique=True)


class Report(Base):
    __tablename__ = "report"

    report_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    type = Column(Integer)
    title = Column(VARCHAR(30))
    content = Column(VARCHAR(255))


class Blog(Base):
    __tablename__ = "blog"

    blog_id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(30))
    content = Column(VARCHAR(255))










