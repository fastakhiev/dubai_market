import ormar
from app.core.db import base_ormar_config
from uuid import UUID, uuid4
from app.models.users import User
from app.models.products import Product
from datetime import datetime


class Question(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="questions")
    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    buyer_id: User = ormar.ForeignKey(User, ondelete="CASCADE")
    product_id: Product = ormar.ForeignKey(Product, ondelete="CASCADE")
    question: str = ormar.String(max_length=500, nullable=False)
    answer: str = ormar.String(max_length=500, nullable=True)
    created_at: datetime = ormar.DateTime(nullable=False, default=datetime.now)
