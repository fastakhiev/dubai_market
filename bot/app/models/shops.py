import ormar
from app.core.db import base_ormar_config
from app.models.users import User
import datetime
from uuid import uuid4, UUID


class Shop(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="shops")
    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    name: str = ormar.String(max_length=100, nullable=False)
    photo: str = ormar.String(max_length=100, nullable=False)
    description: str = ormar.String(max_length=512, nullable=True)
    social_networks: str = ormar.String(max_length=1000, nullable=True)
    user_id: User = ormar.ForeignKey(User, ondelete="CASCADE")
    created_at: datetime.datetime = ormar.DateTime(
        nullable=False, default=datetime.datetime.now
    )
    is_moderation: bool = ormar.Boolean(nullable=False)
    is_verified: bool = ormar.Boolean(nullable=False)
    is_active: bool = ormar.Boolean(nullable=False)
