import ormar
from app.core.db import base_ormar_config
from uuid import UUID, uuid4
from app.models.users import User
from datetime import datetime
from decimal import Decimal


class Product(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="products")
    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    title: str = ormar.String(max_length=255, nullable=False)
    description: str = ormar.Text(nullable=True)
    price: Decimal = ormar.Decimal(precision=10, scale=2, nullable=False)
    currency: str = ormar.String(max_length=10, nullable=False)
    seller_id: User = ormar.ForeignKey(User)
    status: str = ormar.String(max_length=50, nullable=False)
    photos: list = ormar.JSON(nullable=True)
    category: str = ormar.String(max_length=100, nullable=False)
    created_at: datetime = ormar.DateTime(nullable=False, default=datetime.now())
    updated_at: datetime = ormar.DateTime(nullable=False, default=datetime.now())
