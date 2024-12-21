from fastapi import Header, HTTPException


def get_session_token(x_session_token: str = Header(...)):
    if not x_session_token:
        raise HTTPException(status_code=400, detail="X-Session-Token header missing")
    return x_session_token


def get_user():
    pass
