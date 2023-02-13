from sqlalchemy.orm import Session
import app.models as models
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
    db_report = models.Report(user_id=user.user_id, title=report.title, content=report.content, type=report.type,
                              lng=report.lng, lat=report.lat, country=report.country, image1=report.image1,
                              image2=report.image2, image3=report.image3, time_created=datetime.datetime.utcnow())
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
    return db.query(models.Report).all()


def get_userid_by_reportid(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.report_id == report_id).first().user_id


def get_report_by_id(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.report_id == report_id).first()



def get_reports_by_country(db: Session, country: str):
    return db.query(models.Report).filter(models.Report.country == country).all()


def create_new_blog(db: Session, blog: schemas.BlogBase):
    db_blog = models.Blog(title=blog.title, content=blog.content)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def get_all_blogs(db: Session):
    return db.query(models.Blog).all()


def get_blog_by_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()



def delete_blog_by_id(db:Session, blog: schemas.Blog):
    db.delete(blog)
    db.commit()