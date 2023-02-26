import datetime
from sqlalchemy import Column, TEXT, Integer, BINARY, VARCHAR, Float, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class UserCreds(Base):
    __tablename__ = "user_creds"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(VARCHAR(30), unique=True)
    password = Column(BINARY(60))
    fullname = Column(VARCHAR(30))

    report = relationship("Report", back_populates="user")


class Report(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_creds.user_id"))
    type = Column(VARCHAR(255))
    content = Column(VARCHAR(255))
    lng = Column(Float)
    lat = Column(Float)
    country = Column(VARCHAR(30))
    image1 = Column(TEXT)
    image2 = Column(TEXT)
    image3 = Column(TEXT)
    expiry_time = Column(DateTime, default=datetime.datetime(2022, 12, 28))
    time_created = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserCreds", back_populates="report")
