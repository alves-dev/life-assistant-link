from fastapi import Header, HTTPException
from app.config.setting import setting


API_KEY = setting.API_KEY


def authentication(api_key: str = Header(...)):
    if api_key == API_KEY:
        return True
    else:
        raise HTTPException(status_code=401, detail="API Key invalid")
