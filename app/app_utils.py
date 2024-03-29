from datetime import timedelta, datetime
import jwt
from better_profanity import profanity
secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
algorithm = "HS256"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_access_token(*, data: str):
    to_decode = data
    payload = jwt.decode(to_decode, secret_key, algorithms=[algorithm])
    username = payload.get("sub")
    return username


# Implement Hatespeech detection in this function
def detect_hatespeech(data: str):
    return profanity.contains_profanity(data)


# This function needs to be improved to cater for various types of events
def det_expiry(event_type: str):
    expiry = datetime.utcnow()
    match event_type:
        case "Demonstration":
            expiry = expiry + timedelta(days=2)
        case "Traffic Accident":
            expiry = expiry + timedelta(days=1)
        case "Explosion":
            expiry = expiry + timedelta(days=3)
        case "Violent Demonstration":
            expiry = expiry + timedelta(days=3)
        case "Chemical Hazard":
            expiry = expiry + timedelta(days=5)
        case "Natural Catastrophe":
            expiry = expiry + timedelta(days=7)
        case _:
            expiry = expiry + timedelta(days=7)
    return expiry





