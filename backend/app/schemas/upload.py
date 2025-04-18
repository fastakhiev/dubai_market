from pydantic import BaseModel

class UploadImage(BaseModel):
    file_id: str
