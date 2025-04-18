import ormar
from app.core.db import base_ormar_config
from uuid import UUID, uuid4


class Photo(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="photos")
    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    file_id: str = ormar.String(max_length=1000, nullable=False)
    file_name: str = ormar.String(max_length=500, nullable=False)
