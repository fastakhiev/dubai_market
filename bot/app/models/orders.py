import ormar
from app.core.db import base_ormar_config
from app.models.users import User
from app.models.products import Product
import datetime
from uuid import uuid4, UUID


class Order(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="orders")
    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    product_id: Product = ormar.ForeignKey(Product, ondelete="CASCADE")
    buyer_id: User = ormar.ForeignKey(User, ondelete="CASCADE")
    destination: str = ormar.String(max_length=500, nullable=False)
    seller_comment: str = ormar.String(max_length=500, nullable=True)
    buyer_comment: str = ormar.String(max_length=500, nullable=True)
    is_approve: bool = ormar.Boolean(nullable=False)
    created_at: datetime.datetime = ormar.DateTime(nullable=False, default=datetime.datetime.now)
