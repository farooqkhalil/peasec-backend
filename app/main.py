import uvicorn
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
import app.crud as crud
import app.models as models
import app.schemas as schemas
from app.app_utils import decode_access_token, create_access_token, detect_hatespeech
from app.crud import get_user_by_username
from app.database import engine, SessionLocal
from app.schemas import UserInfo, TokenData, UserCreate, Token



models.Base.metadata.create_all(bind=engine)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(debug=True)

# Dependency


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate", scheme_name= "JWT")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> UserInfo:
        isTokenValid: bool = False

        try:
            payload = decode_access_token(data=token)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return payload


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
   user = get_user_by_username(db, username=decode_access_token(data=token))
   return user


# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = decode_access_token(data=token)
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except PyJWTError:
#         raise credentials_exception
#     user = get_user_by_username(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


@app.post("/user", response_model=UserInfo)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.post("/authenticate", response_model=Token)
def authenticate_user(user: schemas.UserAuthenticate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")
    else:
        is_password_correct = crud.check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password is not correct")
        else:
            from datetime import timedelta
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "Bearer"}


@app.post("/report", dependencies=[Depends(JWTBearer())], response_model=schemas.Report)
async def create_new_report(report: schemas.ReportBase, db: Session = Depends(get_db), current_user: UserInfo = Depends(get_current_user)):
    if detect_hatespeech(report.title) or detect_hatespeech(report.content):
        raise HTTPException(status_code=406, detail="Offensive Content not allowed")
    return crud.create_new_report(db=db, report=report, user=current_user)

@app.post("/delete/{id}", dependencies=[Depends(JWTBearer())], response_model=int)
async def delete_report_by_id(report_id, db: Session = Depends(get_db), current_user: UserInfo = Depends(get_current_user)):
    if (crud.get_report_by_id(db, report_id=report_id) == None):
        raise HTTPException(status_code=404, detail="report does not exist")
    elif current_user.user_id == crud.get_userid_by_reportid(db=db, report_id=report_id):
        return crud.delete_report_by_id(db=db, report_id=report_id)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


# current_user: UserInfo = Depends(get_current_user),
@app.get("/get_reports")
async def get_all_reports(db: Session = Depends(get_db)):
    return crud.get_all_reports(db=db)


# , current_user: UserInfo = Depends(get_current_user)
@app.get("/report_by_country/{country}")
async def get_reports_by_country(country, db: Session = Depends(get_db)):
    return crud.get_reports_by_country(db=db, country=country)


# , current_user: UserInfo = Depends(get_current_user)
@app.get("/report/{report_id}")
async def get_report_by_id(report_id
                         , db: Session = Depends(get_db)):
    return crud.get_report_by_id(db=db, report_id=report_id)

#
# # , current_user: UserInfo = Depends(get_current_user)
# # @app.post("/blog", response_model=schemas.Blog)
# async def create_new_blog(blog: schemas.BlogBase
#                           , current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
#     return crud.create_new_blog(db=db, blog=blog)
#
#
# # current_user: UserInfo = Depends(get_current_user),
# # @app.get("/blog")
# async def get_all_blogs(db: Session = Depends(get_db)):
#     return crud.get_all_blogs(db=db)
#

# # @app.get("/blog/{blog_id}")
# async def get_blog_by_id(blog_id, current_user: UserInfo = Depends(get_current_user)
#                          , db: Session = Depends(get_db)):
#     return crud.get_blog_by_id(db=db, blog_id=blog_id)
#
#
# # @app.delete("/blog/{blog_id}",status_code=204)
# async def delete_blog_by_id(blog_id, current_user: UserInfo = Depends(get_current_user)
#                          , db: Session = Depends(get_db)):
#     blog_delete = crud.get_blog_by_id(db=db,blog_id=blog_id)
#     if blog_delete:
#         crud.delete_blog_by_id(db=db,blog=blog_delete)


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run(app, log_config=log_config)
