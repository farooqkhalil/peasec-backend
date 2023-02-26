from sqlalchemy.orm import Session
import app.models as models
from app.app_utils import det_expiry
from app.models import Report
import app.schemas as schemas
import bcrypt
import datetime


def get_user_by_username(db: Session, username: str):
    return db.query(models.UserCreds).filter(models.UserCreds.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.UserCreds(username=user.username, password=hashed_password, fullname=user.fullname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_username_password(db: Session, user: schemas.UserAuthenticate):
    db_user_info: models.UserCreds = get_user_by_username(db, username=user.username)
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password)


def create_new_report(db: Session, report: schemas.ReportBase, user: schemas.UserInfo):
    db_report = models.Report(user_id=user.user_id, type=report.type, content=report.content,
                              lng=report.lng, lat=report.lat, country=report.country, image1=report.image1,
                              image2=report.image2, image3=report.image3, expiry_time=det_expiry(report.type),
                              time_created=datetime.datetime.utcnow())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def delete_report_by_id(db: Session, report_id: int):
    db_report = get_report_by_id(db, report_id=report_id)
    id=report_id
    db.delete(db_report)
    db.commit()
    return id


def get_all_reports(db: Session):
    return db.query(models.Report).filter(models.Report.expiry_time > datetime.datetime.utcnow()).all()


def get_userid_by_reportid(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.report_id == report_id).first().user_id


def get_report_by_id(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.report_id == report_id).first()


def get_reports_by_country(db: Session, country: str):
    return get_all_reports(db=db).filter(models.Report.country == country).all()
