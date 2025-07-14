import ormar
from app.core.db import base_ormar_config
import datetime
from uuid import uuid4, UUID


class User(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="users")
    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    telegram_id: str = ormar.String(max_length=100, nullable=False, unique=True)
    full_name: str = ormar.String(max_length=100, nullable=False)
    phone: str = ormar.String(max_length=100, nullable=False)
    passport: str = ormar.String(max_length=1000, nullable=True)
    created_at: datetime.datetime = ormar.DateTime(
        nullable=False, default=datetime.datetime.now
    )
    is_active: bool = ormar.Boolean(nullable=False)
