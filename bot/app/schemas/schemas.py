from pydantic import BaseModel

class BanUser(BaseModel):
    telegram_id: str
